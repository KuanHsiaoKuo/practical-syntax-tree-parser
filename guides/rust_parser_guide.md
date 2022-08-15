# Practical Syntax Tree Parser

<!-- toc start -->

* [配合指令](#配合指令)
* [总体设计](#总体设计)
    * [常见代码组织形式](#常见代码组织形式)
        * [单文件](#单文件)
        * [多文件模块化：库/package/crate](#多文件模块化：库/package/crate)
        * [项目/框架](#项目/框架)
* [Rust篇](#Rust篇)
    * [单文件解析](#单文件解析)
    * [crate解析](#crate解析)
        * [crate命名与引用](#crate命名与引用)
        * [本crate内代码引用](#本crate内代码引用)
        * [非本crate内代码引用](#非本crate内代码引用)
            * [src/main.rs 与 src/lib.rs](#src/main.rs 与 src/lib.rs)
            * [mod.rs](#mod.rs)
    * [项目解析](#项目解析)
    * [语法关键词](#语法关键词)
        * [use 与 pub  (crate) use](#use 与 pub  (crate) use)
        * [pub mod](#pub mod)

<!-- toc end -->

## 配合指令

```shell
find . -name 'mod.rs'
```

## 总体设计

> 这种解析首先需要掌握编程语言的模块系统，然后根据模块系统分割出来的文件内容再使用编程语法进行入微解析

### 常见代码组织形式

#### 单文件

这种主要考虑单纯的语法关键字进行解析。无非就是分为过程、对象昂、函数三种范式，最大的封装不过是对应的函数定义、trait定义与实现等。

#### 多文件模块化：库/package/crate

这点主要是单文件过长而需要分成多个代码文件的情况。主要注意标志文件：

- rust的Cargo.toml+src/mod.rs/lib.rs/main.rs
- python的__init__
- golang
- typescript

还需要注意代码搜索路径

#### 项目/框架

这种情况主要是模块之间的联系，也是最顶层的设计。

## Rust篇

### 单文件解析

### crate解析

#### crate命名与引用

值得注意的是，使用​​extern crate​​声明包的名称是linked_list，用的是​​下划线​​“​​_
​​”，而在Cargo.toml中用的是​​连字符​​“​​-​​”。其实Cargo默认会把​​连字符​​转换成​​下划线​​。

Rust也不建议以“​​-rs​​”或“​​_rs​​”为后缀来命名包名，而且会强制性的将此后缀去掉。

- [Rust太难？那是你没看到这套Rust语言学习万字指南！_mb5fed73533dfa9的技术博客_51CTO博客](https://blog.51cto.com/u_15072927/4607530)
- [<Rust编程之道>](marginnote3app://note/3D3F7585-0DC8-4E24-B24B-AA8DD79EED3A)

#### 本crate内代码引用

#### 非本crate内代码引用

主要根据cargo.toml文件中定义好的路径/网络路径找到相应文件。

##### src/main.rs 与 src/lib.rs

Cargo 遵循的一个约定：src/main.rs 就是一个与包同名的二进制 crate 的 crate 根。同样的，Cargo 知道如果包目录中包含 src/lib.rs，则包带有与其同名的库 crate，且 src/lib.rs 是
crate 根。
如果一个包同时含有 src/main.rs 和 src/lib.rs，则它有两个 crate：一个库和一个二进制项，且名字都与包相同。

crate关键字在不同crate中含义不同。
在库crate中，代表的是lib.rs；在二进制crate中，代表的是main.rs。

使用自己的crate名代表的是其库crate
假设crate名为xxtest，那么xxtest::name()也就是在调用库crate中的函数name。

值得一提的是，自己的crate名在只有在main.rs和lib.rs同时存在的时候才会赋予特殊的含义，并只在二进制crate中可用；

值得二提的是，当存在一个和crate名同名的模块时，会优先调用模块里的东西。

顺带提一嘴，使用mod lib并不能变为一个普通模块，但是你可以使用crate::lib来访问模块了，虽然我并不建议你这么用。

- [Rust模块系统-当main.rs和lib.rs同时存在的坑 - 知乎](https://zhuanlan.zhihu.com/p/351091783)

##### mod.rs

1. mod.rs 类似于python的package中必备的__init__.py。在rust 2015版本时，一个模块还需要一个mod.rs文件来告诉编译器，这是一个模块。mod.rs中将会告诉这个模块的名称，以及可被外部调用的代码。
2. 如下所示

```shell
tree -L 1 tracing/src/logging/layers                                                                                                                                                                                                   ─╯
tracing/src/logging/layers
├── mod.rs
└── prefix_layer.rs
```

```rust
// 将prefix_layer文件看作一个mod
mod prefix_layer;

// 指明这个mod中哪些可被看见
pub use prefix_layer::*;
```

- [module - In Rust, what is the purpose of a mod.rs file? - Stack Overflow](https://stackoverflow.com/questions/26435102/in-rust-what-is-the-purpose-of-a-mod-rs-file)
- [《Rust编程之道》- 10.2 模块系统节选](marginnote3app://note/22F82B77-B1E1-43AB-9E8E-D0EB199974B7)

### 项目解析

以substrate，其实一个项目直接就是最顶层的crate+代码文件目录构成。这里的代码文件目录只是用来直观分开放crate，在编译时只是根据相对路径来找到代码文件。

### 语法关键词

#### use 与 pub  (crate) use

1. use: 引入
2. pub use T 导出了 T，T 可以被其他 crate 使用；
3. pub (crate) use T 只把 T 导出到当前的 crate，其他 crate 访问不了

- [ rust语句 pub (crate) use 和 pub use有什么区别？ - 知乎](https://www.zhihu.com/question/511958558/answer/2341181598)

#### pub mod

pub mod xxx ;相当于把xxx复制到这个pub mod语句处 再冠以pub (这个比较好理解)

#### workspace/members

```toml
[workspace]
resolver = "2"

members = [
    "client/db"
]
```