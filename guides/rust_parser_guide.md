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

### 单文件解析(main/lib/mod同名文件)

#### mod同名文件

1. lib/main中：同级目录 > mod同名文件
2. 非lib/main中：同级目录 > 同名目录 > mod同名文件

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

### Cargo.toml

#### workspace介绍

- [Cargo Reference笔记: 工作区 | Rust学习笔记](https://skyao.io/learning-rust/docs/build/cargo/cargo-book/reference-workspaces.html)

1. 所有软件包共享一个共同的 Cargo.lock 文件，该文件驻留在工作区根部。

2. 所有软件包共享一个共同的输出目录，该目录默认为工作区根目录下的target。

3. Cargo.toml 中的 [patch]、[replace] 和 [profile.*] 部分只在根清单中被识别，而在 crate 的清单中被忽略。

#### profile

- [发布配置 Profile - Rust语言圣经(Rust Course)](https://course.rs/cargo/reference/profiles.html)

### mod与use的区别

- [Rust 中 Mod 和 Use 的区别 | D栈 - Delft Stack](https://www.delftstack.com/zh/howto/rust/rust-mod-vs-use/)

> 它们之间的主要区别在于 use 从外部库导入模块，而 mod 创建只能在当前文件中使用的内部模块。

1. use: use 将另一个项目添加到当前命名空间, 是一种动态加载机制
2. mod: 模块允许你将代码组织到单独的文件中。它们将你的代码划分为可以在其他模块或程序中导入和使用的逻辑部分。

简而言之，mod 用于指定模块和子模块，以便你可以在当前的 .rs 文件中使用它们
Rust 中的模块只不过是零个或多个事物的容器。这是一种逻辑组织项目的方法，因此你的模块可以轻松遍历。

模块可用于创建 crate 的树结构，使你能够在必要时将工作拆分到任意深度的多个文件中。单个 .rs 文件可以包含多个模块，或者单个文件可以包含多个模块。

最后，你可以使用 mod 对对象进行逻辑分组。你可以在单个 .rs 文件中构建 mod 块，或者你可以将源代码划分为多个 .rs 文件，使用 mod，并让 Cargo 生成你的 crate 的树结构。

### 模块系统理解

> [Rust 模块系统理解 - 知乎](https://zhuanlan.zhihu.com/p/443926839)

- Rust编译器只接受一个源文件，输出一个crate
- 每一个crate都有一个匿名的根命名空间，命名空间可以无限嵌套
- “mod mod-name { ... }“ 将大括号中的代码置于命名空间mod-name之下
- “use mod-name1::mod-name2;" 可以打开命名空间，减少无休止的::操作符
- “mod mod-name;“ 可以指导编译器将多个文件组装成一个文件
- “pub use mod-nam1::mod-name2::item-name;“
  语句可以将mod-name2下的item-name提升到这条语句所在的空间，item-name通常是函数或者结构体。Rust社区通常用这个方法来缩短库API的命名空间深度
- 编译器规定use语句一定要在mod语句之前

### 从cargo new开始说

- [Rust中的代码组织:package/crate/mod - 菩提树下的杨过 - 博客园](https://www.cnblogs.com/yjmyzz/p/rust_package_crate_mod.html)

> [本地批注地址](x-devonthink-item://0FB4BFD2-C96E-4DFA-A8E9-09BFBAD1BBF9)

#### package、crate、mod、use

1. package: cargo 创建一个新项目时，默认就创建了一个package
2. crate: 默认由一个Cargo.toml文件对应
3. mod: 在crate里，又可以创建一堆所谓的mod(模块)

![img](https://raw.githubusercontent.com/KuanHsiaoKuo/writing_materials/main/imgs/27612-20211106113206098-804387811.png)

- 1个Package里，至少要有1种Crate(要么是Library Crate，要么是Binary Crate)
- 1个Package里，最多只能有1个Library Crate
- 1个Package里，可以有0或多个Binary Crate
- 1个Crate里，可以创建0或多个mod(后面还会详细讲mod)

> 1个package里，允许有1个library crate和多个binary crate

4.mod还有一种重新确定隐私的作用
> 比如mod同名目录下的模块，可以在mod同名文件中将子mod"复制"进来后，重新以mod的方式来被外部引入

5. 下面以substrate的frame为例, 说明这种重新确定引入路径的方式：

> 从这里可以看出，rust确实做到了内聚性，引用其他crate的时候，只需要看lib.rs提供了什么，不用关注对应底层源码到底怎么写的。

- frame/executive/src/lib.rs

```rust
use frame_support::{
    dispatch::PostDispatchInfo,
    traits::{
        EnsureInherentsAreFirst, ExecuteBlock, OffchainWorker, OnFinalize, OnIdle, OnInitialize,
        OnRuntimeUpgrade,
    },
    weights::{DispatchClass, DispatchInfo, GetDispatchInfo},
};
```

- frame/executive/Cargo.toml

```toml
frame-support = { version = "4.0.0-dev", default-features = false, path = "../support" }
```

- frame/support/src/lib.rs

```rust
pub mod traits;
```

- frame/support/src/traits.rs
> 这里就将misc::ExecuteBlock等元素提升给traits。
> 而且这种方式还可以有效指定哪些元素可以通过traits暴露出去
```rust
mod misc;

pub use misc::{
    defensive_prelude::{self, *},
    Backing, ConstBool, ConstI128, ConstI16, ConstI32, ConstI64, ConstI8, ConstU128, ConstU16,
    ConstU32, ConstU64, ConstU8, DefensiveSaturating, EnsureInherentsAreFirst, EqualPrivilegeOnly,
    EstimateCallFee, ExecuteBlock, ExtrinsicCall, Get, GetBacking, GetDefault, HandleLifetime,
    IsSubType, IsType, Len, OffchainWorker, OnKilledAccount, OnNewAccount, PreimageProvider,
    PreimageRecipient, PrivilegeCmp, SameOrOther, Time, TryCollect, TryDrop, TypedGet, UnixTime,
    WrapperKeepOpaque, WrapperOpaque,
};
```

- frame/support/src/traits/misc.rs

```rust
pub trait ExecuteBlock<Block: BlockT> {
    /// Execute the given `block`.
    ///
    /// This will execute all extrinsics in the block and check that the resulting header is
    /// correct.
    ///
    /// # Panic
    ///
    /// Panics when an extrinsics panics or the resulting header doesn't match the expected header.
    fn execute_block(block: Block);
}
```

#### 入口函数：fn main() {...}

1. main.rs里面的main函数才会被识别为入口
2. 其他rs文件里面的main函数不会被识别，除非放在bin文件夹中。

> 此时会有多个入口，运行时需要指明