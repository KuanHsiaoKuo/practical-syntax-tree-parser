# 具象语法树解析器(Practical Syntax Tree Parser)

> 主要通过正则提取的方式，基于编程语言语法进行解析与后续的puml具象化

## 预备支持语言

- RUST
- Golang
- Python
- Javascript
- Typescript

## 使用toml配置解析规则

- [TOML/toml-v1.0.0.md at 龙腾道-译 · LongTengDao/TOML](https://github.com/LongTengDao/TOML/blob/%E9%BE%99%E8%85%BE%E9%81%93-%E8%AF%91/toml-v1.0.0.md)

## Rust语法细节梳理

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

#### package、crate、mod

1. package: cargo 创建一个新项目时，默认就创建了一个package
2. crate: 默认由一个Cargo.toml文件对应
3. mod: 在crate里，又可以创建一堆所谓的mod(模块)

![img](https://raw.githubusercontent.com/KuanHsiaoKuo/writing_materials/main/imgs/27612-20211106113206098-804387811.png)

- 1个Package里，至少要有1种Crate(要么是Library Crate，要么是Binary Crate)
- 1个Package里，最多只能有1个Library Crate
- 1个Package里，可以有0或多个Binary Crate
- 1个Crate里，可以创建0或多个mod(后面还会详细讲mod)

> 1个package里，允许有1个library crate和多个binary crate

#### 入口函数：fn main() {...}

1. main.rs里面的main函数才会被识别为入口
2. 其他rs文件里面的main函数不会被识别，除非放在bin文件夹中。

> 此时会有多个入口，运行时需要指明