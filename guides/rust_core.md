# Rust核心

> 静态->泛型->trait->trait bound->trait object: struct、enum和impl

<!-- toc start -->

* [核心思路](#核心思路)
    * [从静态语言开始](#从静态语言开始)
    * [为了复用，加入泛型](#为了复用，加入泛型)
    * [为了范围，加入接口/trait](#为了范围，加入接口/trait)
    * [泛型+trait限定会导致编译的包膨胀，于是考虑trait对象](#泛型+trait限定会导致编译的包膨胀，于是考虑trait对象)
    * [为了隐私，加入pub](#为了隐私，加入pub)
* [泛型-Generic Types](#泛型-Generic Types)
    * [泛型由来](#泛型由来)
    * [泛型使用](#泛型使用)
        * [范型结构体](#范型结构体)
        * [范型枚举体](#范型枚举体)
        * [范型方法(impl)](#范型方法(impl))
    * [泛型的性能表现](#泛型的性能表现)
* [区分一下类的组合与trait的组合](#区分一下类的组合与trait的组合)
* [Trait](#Trait)
    * [关键字](#关键字)
        * [定义](#定义)
        * [实现](#实现)
        * [与实现方法的区别](#与实现方法的区别)
    * [举例](#举例)
    * [限制：孤儿原则](#限制：孤儿原则)
    * [常用方式](#常用方式)
        * [在trait定义中编写默认方法逻辑](#在trait定义中编写默认方法逻辑)
        * [作为函数入参:](#作为函数入参:)
            * [&impl](#&impl)
        * [语法糖：trait限定(trait bounds)](#语法糖：trait限定(trait bounds))
            * [使用T代称](#使用T代称)
            * [使用“+”组合继承](#使用“+”组合继承)
            * [使用where后置](#使用where后置)
        * [作为函数出参](#作为函数出参)
            * [条件出参](#条件出参)
        * [泛型trait多态](#泛型trait多态)
* [Trait Objects](#Trait Objects)
    * [关键字](#关键字)
    * [存在形式](#存在形式)
    * [举例](#举例)
    * [面向对象编程应用(trait objects + struct/enum)](#面向对象编程应用(trait objects + struct/enum))
        * [trait objects 其实就是鸭子类型](#trait objects 其实就是鸭子类型)
* [trait object 与 trait bound的对比](#trait object 与 trait bound的对比)
* [impl使用场景：实现方法，而非函数。](#impl使用场景：实现方法，而非函数。)
    * [结构体/枚举体：定义并实现方法](#结构体/枚举体：定义并实现方法)
    * [结构体/枚举体+trait：实现接口定义的方法](#结构体/枚举体+trait：实现接口定义的方法)
* [Rust面向对象](#Rust面向对象)
    * [注意：可以使用图表，对比python和rust的对应面向对象特性实现方式](#注意：可以使用图表，对比python和rust的对应面向对象特性实现方式)
        * [属性方法](#属性方法)
        * [静态方法](#静态方法)
        * [实例方法](#实例方法)
        * [类方法](#类方法)
    * [Encapsulation](#Encapsulation)
        * [Start from the crate root](#Start from the crate root)
        * [Declaring modules](#Declaring modules)
        * [Declaring submodules](#Declaring submodules)
        * [Paths to code in modules](#Paths to code in modules)
        * [Private vs public](#Private vs public)
        * [The use keyword](#The use keyword)
    * [Inheritance](#Inheritance)
        * [Reuse](#Reuse)
        * [Polymorphism](#Polymorphism)

<!-- toc end -->

## 核心思路

- 所有权、借用、切片
- 泛型、trait、生命周期

### 从静态语言开始

每个方法都需要指定特定类型

### 为了复用，加入泛型

可以用泛型指定所有类型，就不需要重复写同样的方法

### 为了范围，加入接口/trait

其实写方法就是为了写特定操作，那么不如把操作作为重点，于是就有了接口

### 泛型+trait限定会导致编译的包膨胀，于是考虑trait对象

- [精通rust-4.6 使用trait对象实现真正多态性](marginnote3app://note/17559D64-980D-4EA7-B69E-49D766438399)

> 特征和泛型通过单态化(早期绑定)或运行时多态(后期绑定)
>
提供了两种代码复用的方式。何时使用它们取决于具体情况和相关应用程序的需求。通常,错误类型会被分配到动态分发的序列,因为它们应该是很少被执行的代码路径。单态化对小型的应用场景来说非常方便,但是缺点是导致了代码的膨胀和重复,这会影响缓存效率,并增加二进制文件的大小。但是,在这两个选项中,静态分发应该是首选,除非系统对二进制文件大小存在严格的限制。

### 为了隐私，加入pub

## 一、泛型-Generic Types

### 泛型由来

> 泛型本质上是对多类型的抽象，因为对于静态语言来说需要指明类型，对于那些很多类型通用的函数，不能一个个地写出来，那样编写、维护很麻烦。这个时候就需要用泛型了。

```rust
fn largest_i32(list: &[i32]) -> &i32 {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn largest_char(list: &[char]) -> &char {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}


fn largest<T>(list: &[T]) -> &T {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

```

### 泛型使用

#### 范型结构体

```rust
struct Point<T, U> {
    x: T,
    y: U,
}
```

#### 范型枚举体

```rust

enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

#### 范型方法(impl)

> 注意，这里不是泛型函数。本质是因为方法是需要调用者，也就是某个对象；而函数是自己调用。

```rust
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

fn main() {
    let p = Point { x: 5, y: 10 };

    println!("p.x = {}", p.x());
}
```

### 泛型的性能表现

- [Generic Data Types - The Rust Programming Language](https://doc.rust-lang.org/book/ch10-01-syntax.html#performance-of-code-using-generics)

## 区分一下类的组合与trait的组合

```rust
struct Point<X1, Y1> {
    x: X1,
    y: Y1,
}

```

```rust
pub fn notify(item: &(impl Summary + Display)) {}
```

## 二、Trait

-
    - [Traits: Defining Shared Behavior - The Rust Programming Language](https://doc.rust-lang.org/book/ch10-02-traits.html)

> A trait defines functionality a particular type has and can share with other types. We can use traits to define shared
> behavior in an abstract way. We can use trait bounds to specify that a generic type can be any type that has certain
> behavior.

> Traits are similar to a feature often called interfaces in other languages, although with some differences.

### 关键字

#### 定义

trait

#### 实现

impl <trait name> for <struct name>{ fn <method_name in trait definition> }

#### 与实现方法的区别

Implementing a trait on a type is similar to implementing regular methods. The difference is that after impl, we put the
trait name we want to implement, then use the for keyword, and then specify the name of the type we want to implement
the trait for. Within the impl block, we put the method signatures that the trait definition has defined. Instead of
adding a semicolon after each signature, we use curly brackets and fill in the method body with the specific behavior
that we want the methods of the trait to have for the particular type.

### 举例

```rust
pub trait Summary {
    fn summarize(&self) -> String;
}

pub struct NewsArticle {
    pub headline: String,
    pub location: String,
    pub author: String,
    pub content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.headline, self.author, self.location)
    }
}

pub struct Tweet {
    pub username: String,
    pub content: String,
    pub reply: bool,
    pub retweet: bool,
}

impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}


use aggregator::{Summary, Tweet};

fn main() {
    let tweet = Tweet {
        username: String::from("horse_ebooks"),
        content: String::from(
            "of course, as you probably already know, people",
        ),
        reply: false,
        retweet: false,
    };

    println!("1 new tweet: {}", tweet.summarize());
}


```

### 限制：孤儿原则

we can’t implement external traits on external types. For example, we can’t implement the Display trait on Vec<T> within
our aggregator crate, because Display and Vec<T> are both defined in the standard library and aren’t local to our
aggregator crate. This restriction is part of a property called coherence (相干) , and more specifically the orphan (孤儿)
rule, so named because the parent type is not present. This rule ensures that other people’s code can’t break your code
and vice (副) versa. Without the rule, two crates could implement the same trait for the same type, and Rust wouldn’t
know which implementation to use.

### 常用方式

#### 在trait定义中编写默认方法逻辑

#### 作为函数入参:

##### &impl

```rust
pub fn notify(item: &impl Summary) {
    println!("Breaking news! {}", item.summarize());
}
```

#### 语法糖：trait限定(trait bounds)

##### 使用T代称

```rust
pub fn notify<T: Summary>(item1: &T, item2: &T) {}
```

##### 使用“+”组合继承

```rust
pub fn notify(item: &(impl Summary + Display)) {}
```

##### 使用where后置

```rust
fn some_function<T, U>(t: &T, u: &U) -> i32
    where T: Display + Clone,
          U: Clone + Debug
{}

```

#### 作为函数出参

```rust
fn returns_summarizable() -> impl Summary {
    Tweet {
        username: String::from("horse_ebooks"),
        content: String::from(
            "of course, as you probably already know, people",
        ),
        reply: false,
        retweet: false,
    }
}
```

##### 条件出参

```rust
fn returns_summarizable(switch: bool) -> impl Summary {
    if switch {
        NewsArticle {
            headline: String::from(
                "Penguins win the Stanley Cup Championship!",
            ),
            location: String::from("Pittsburgh, PA, USA"),
            author: String::from("Iceburgh"),
            content: String::from(
                "The Pittsburgh Penguins once again are the best \
                 hockey team in the NHL.",
            ),
        }
    } else {
        Tweet {
            username: String::from("horse_ebooks"),
            content: String::from(
                "of course, as you probably already know, people",
            ),
            reply: false,
            retweet: false,
        }
    }
}
```

#### 泛型trait多态

> 根据泛型的trait设定不同函数

```rust
use std::fmt::Display;

struct Pair<T> {
    x: T,
    y: T,
}

impl<T> Pair<T> {
    fn new(x: T, y: T) -> Self {
        Self { x, y }
    }
}

impl<T: Display + PartialOrd> Pair<T> {
    fn cmp_display(&self) {
        if self.x >= self.y {
            println!("The largest member is x = {}", self.x);
        } else {
            println!("The largest member is y = {}", self.y);
        }
    }
}
```

## 三、Trait Objects

- [Trait object types - The Rust Reference](https://doc.rust-lang.org/stable/reference/types/trait-object.html)

> A trait object is an opaque value of another type that implements a set of traits. The set of traits is made up of an
> object safe base trait plus any number of auto traits.

### 关键字

dyn Trait

> Before the 2021 edition, the dyn keyword may be omitted .

### 存在形式

```rust
dyn Trait
dyn Trait + Send
dyn Trait + Send + Sync
dyn Trait + 'static
dyn Trait + Send + 'static
dyn Trait +
dyn 'static + Trait.
dyn (Trait)
```

### 举例

```rust
trait Printable {
    fn stringify(&self) -> String;
}

impl Printable for i32 {
    fn stringify(&self) -> String { self.to_string() }
}

fn print(a: Box<dyn Printable>) {
    println!("{}", a.stringify());
}

fn main() {
    print(Box::new(10) as Box<dyn Printable>);
}
```

### 面向对象编程应用(trait objects + struct/enum)

- [Using Trait Objects That Allow for Values of Different Types - The Rust Programming Language](https://doc.rust-lang.org/book/ch17-02-trait-objects.html)

> We can use trait objects in place of a generic or concrete type.

Wherever we use a trait object, Rust’s type system will ensure at compile time that any value used in that context will
implement the trait object’s trait. Consequently, we don’t need to know all the possible types at compile time.

> We’ve mentioned that, in Rust, we refrain from calling structs and enums “objects” to distinguish them from other
> languages’ objects.


In a struct or enum, the data in the struct fields and the behavior in impl blocks are separated, whereas in other
languages, the data and behavior combined into one concept is often labeled an object.

However, trait objects are more like objects in other languages in the sense that they combine data and behavior.

But trait objects differ from traditional objects in that we can’t add data to a trait object. Trait objects aren’t as
generally useful as objects in other languages: their specific purpose is to allow abstraction across common behavior.

- trait objects

```rust
pub struct Screen {
    // This vector is of type Box<dyn Draw>
    // which is a trait object; it’s a stand-in for any type inside a Box that implements the Draw trait.
    pub components: Vec<Box<dyn Draw>>,
}

impl Screen {
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();
        }
    }
}
```

- trait bounds

```rust
pub struct Screen<T: Draw> {
    pub components: Vec<T>,
}

// If you’ll only ever have homogeneous collections, 
// using generics and trait bounds is preferable because 
// the definitions will be monomorphized at compile time to use the concrete types.
impl<T> Screen<T>
    where
        T: Draw,
{
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();
        }
    }
}
```

- static or dynamic dispatch

1. trait限定：静态分发，编译期确定，对应实现了trait限定的类型
2. trait对象：动态分发，编译器指针，运行期确定具体类型

```rust
pub fn trait_object() {
    #[derive(Debug)]
    struct Foo;
    trait Bar {
        fn baz(&self);
    }
    impl Bar for Foo {
        fn baz(&self) { println!("{:?}", self) }
    }
    fn static_dispatch<T>(t: &T) where T: Bar {
        t.baz();
    }
    fn dynamic_dispatch(t: &Bar) {
        t.baz();
    }
    let foo = Foo;
    static_dispatch(&foo);
    dynamic_dispatch(&foo);
}

```

#### trait objects 其实就是鸭子类型

> 在编译期编译器就知道你的类型是否具有指定的动作，提前检查

This concept—of being concerned only with the messages a value responds to rather than the value’s concrete type—is
similar to the concept of duck typing in dynamically typed languages:

> if it walks like a duck and quacks like a duck, then it must be a duck!

In the implementation of run on Screen in Listing 17-5, run doesn’t need to know what the concrete type of each
component is.

It doesn’t check whether a component is an instance of a Button or a SelectBox, it just calls the draw method on the
component.

> By specifying Box<dyn Draw> as the type of the values in the components vector, we’ve defined Screen to need values
> that we can call the draw method on.

The advantage of using trait objects and Rust’s type system to write code similar to code using duck typing is that:

- we never have to check whether a value implements a particular method at runtime or worry about getting errors if a
  value doesn’t implement a method but we call it anyway.
- Rust won’t compile our code if the values don’t implement the traits that the trait objects need.

## 四、trait object 与 trait bound的对比

- [Performance of Code Using Generics](https://doc.rust-lang.org/book/ch10-01-syntax.html#performance-of-code-using-generics)
- [Trait Objects Perform Dynamic Dispatch](https://doc.rust-lang.org/book/ch17-02-trait-objects.html#trait-objects-perform-dynamic-dispatch)

Recall in the “Performance of Code Using Generics” section in Chapter 10 our discussion on the monomorphization process
performed by the compiler when we use trait bounds on generics: the compiler generates nongeneric implementations of
functions and methods for each concrete type that we use in place of a generic type parameter. The code that results
from monomorphization is doing static dispatch, which is when the compiler knows what method you’re calling at compile
time. This is opposed to dynamic dispatch, which is when the compiler can’t tell at compile time which method you’re
calling. In dynamic dispatch cases, the compiler emits code that at runtime will figure out which method to call.

When we use trait objects, Rust must use dynamic dispatch. The compiler doesn’t know all the types that might be used
with the code that’s using trait objects, so it doesn’t know which method implemented on which type to call. Instead, at
runtime, Rust uses the pointers inside the trait object to know which method to call. This lookup incurs a runtime cost
that doesn’t occur with static dispatch. Dynamic dispatch also prevents the compiler from choosing to inline a method’s
code, which in turn prevents some optimizations. However, we did get extra flexibility in the code that we wrote in
Listing 17-5 and were able to support in Listing 17-9, so it’s a trade-off to consider.

- tait对象编译期间无法确定对象大小，所以需要使用指针形式(引用)。

> trait作为参数一般有两种写法：

- 一种是trait对象，需要运行时才能获取对象大小属于动态分发，
- 一种是trait限定，类似模板是编译器件确定属于静态分发。

## 五、impl使用场景：实现方法，而非函数。

> impl与fn不会共存

### impl <> xxx<>结构体/枚举体：定义并实现方法

> impl<target types> <struct/enum><target types>

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}
```

```rust
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}
```

#### 示例一: 定义并实现许多方法

- [Executive in frame_executive - Rust](https://paritytech.github.io/substrate/master/frame_executive/struct.Executive.html)

> substrate/frame/executive/src/lib.rs

```rust
impl<
    System: frame_system::Config + EnsureInherentsAreFirst<Block>,
    Block: traits::Block<Header=System::Header, Hash=System::Hash>,
    Context: Default,
    UnsignedValidator,
    AllPalletsWithSystem: OnRuntimeUpgrade
    + OnInitialize<System::BlockNumber>
    + OnIdle<System::BlockNumber>
    + OnFinalize<System::BlockNumber>
    + OffchainWorker<System::BlockNumber>,
    COnRuntimeUpgrade: OnRuntimeUpgrade,
> Executive<System, Block, Context, UnsignedValidator, AllPalletsWithSystem, COnRuntimeUpgrade>
    where
        Block::Extrinsic: Checkable<Context> + Codec,
        CheckedOf<Block::Extrinsic, Context>: Applyable + GetDispatchInfo,
        CallOf<Block::Extrinsic, Context>:
        Dispatchable<Info=DispatchInfo, PostInfo=PostDispatchInfo>,
        OriginOf<Block::Extrinsic, Context>: From<Option<System::AccountId>>,
        UnsignedValidator: ValidateUnsigned<Call=CallOf<Block::Extrinsic, Context>>,
{
    /// Execute all `OnRuntimeUpgrade` of this runtime, and return the aggregate weight.
    pub fn execute_on_runtime_upgrade() -> frame_support::weights::Weight {
        <(COnRuntimeUpgrade, AllPalletsWithSystem) as OnRuntimeUpgrade>::on_runtime_upgrade()
    }

    /// Execute given block, but don't do any of the `final_checks`.
    ///
    /// Should only be used for testing.
    #[cfg(feature = "try-runtime")]
    pub fn execute_block_no_check(block: Block) -> frame_support::weights::Weight {
        Self::initialize_block(block.header());
        Self::initial_checks(&block);

        let (header, extrinsics) = block.deconstruct();

        Self::execute_extrinsics_with_book_keeping(extrinsics, *header.number());

        // do some of the checks that would normally happen in `final_checks`, but definitely skip
        // the state root check.
        {
            let new_header = <frame_system::Pallet<System>>::finalize();
            let items_zip = header.digest().logs().iter().zip(new_header.digest().logs().iter());
            for (header_item, computed_item) in items_zip {
                header_item.check_equal(computed_item);
                assert!(header_item == computed_item, "Digest item must match that calculated.");
            }

            assert!(
                header.extrinsics_root() == new_header.extrinsics_root(),
                "Transaction trie root must be valid.",
            );
        }

        frame_system::Pallet::<System>::block_weight().total()
    }

    /// Execute all `OnRuntimeUpgrade` of this runtime, including the pre and post migration checks.
    ///
    /// This should only be used for testing.
    #[cfg(feature = "try-runtime")]
    pub fn try_runtime_upgrade() -> Result<frame_support::weights::Weight, &'static str> {
        <(COnRuntimeUpgrade, AllPalletsWithSystem) as OnRuntimeUpgrade>::pre_upgrade().unwrap();
        let weight = Self::execute_on_runtime_upgrade();

        <(COnRuntimeUpgrade, AllPalletsWithSystem) as OnRuntimeUpgrade>::post_upgrade().unwrap();

        Ok(weight)
    }

    /// Start the execution of a particular block.
    pub fn initialize_block(header: &System::Header) {
        sp_io::init_tracing();
        sp_tracing::enter_span!(sp_tracing::Level::TRACE, "init_block");
        let digests = Self::extract_pre_digest(header);
        Self::initialize_block_impl(header.number(), header.parent_hash(), &digests);
    }

    fn extract_pre_digest(header: &System::Header) -> Digest {
        let mut digest = <Digest>::default();
        header.digest().logs().iter().for_each(|d| {
            if d.as_pre_runtime().is_some() {
                digest.push(d.clone())
            }
        });
        digest
    }

    fn initialize_block_impl(
        block_number: &System::BlockNumber,
        parent_hash: &System::Hash,
        digest: &Digest,
    ) {
        // Reset events before apply runtime upgrade hook.
        // This is required to preserve events from runtime upgrade hook.
        // This means the format of all the event related storages must always be compatible.
        <frame_system::Pallet<System>>::reset_events();

        let mut weight = 0;
        if Self::runtime_upgraded() {
            weight = weight.saturating_add(Self::execute_on_runtime_upgrade());
        }
        <frame_system::Pallet<System>>::initialize(block_number, parent_hash, digest);
        weight = weight.saturating_add(<AllPalletsWithSystem as OnInitialize<
            System::BlockNumber,
        >>::on_initialize(*block_number));
        weight = weight.saturating_add(
            <System::BlockWeights as frame_support::traits::Get<_>>::get().base_block,
        );
        <frame_system::Pallet<System>>::register_extra_weight_unchecked(
            weight,
            DispatchClass::Mandatory,
        );

        frame_system::Pallet::<System>::note_finished_initialize();
    }

    /// Returns if the runtime was upgraded since the last time this function was called.
    fn runtime_upgraded() -> bool {
        let last = frame_system::LastRuntimeUpgrade::<System>::get();
        let current = <System::Version as frame_support::traits::Get<_>>::get();

        if last.map(|v| v.was_upgraded(&current)).unwrap_or(true) {
            frame_system::LastRuntimeUpgrade::<System>::put(
                frame_system::LastRuntimeUpgradeInfo::from(current),
            );
            true
        } else {
            false
        }
    }

    fn initial_checks(block: &Block) {
        sp_tracing::enter_span!(sp_tracing::Level::TRACE, "initial_checks");
        let header = block.header();

        // Check that `parent_hash` is correct.
        let n = *header.number();
        assert!(
            n > System::BlockNumber::zero() &&
                <frame_system::Pallet<System>>::block_hash(n - System::BlockNumber::one()) ==
                    *header.parent_hash(),
            "Parent hash should be valid.",
        );

        if let Err(i) = System::ensure_inherents_are_first(block) {
            panic!("Invalid inherent position for extrinsic at index {}", i);
        }
    }

    /// Actually execute all transitions for `block`.
    pub fn execute_block(block: Block) {
        sp_io::init_tracing();
        sp_tracing::within_span! {
			sp_tracing::info_span!("execute_block", ?block);

			Self::initialize_block(block.header());

			// any initial checks
			Self::initial_checks(&block);

			let signature_batching = sp_runtime::SignatureBatching::start();

			// execute extrinsics
			let (header, extrinsics) = block.deconstruct();
			Self::execute_extrinsics_with_book_keeping(extrinsics, *header.number());

			if !signature_batching.verify() {
				panic!("Signature verification failed.");
			}

			// any final checks
			Self::final_checks(&header);
		}
    }

    /// Execute given extrinsics and take care of post-extrinsics book-keeping.
    fn execute_extrinsics_with_book_keeping(
        extrinsics: Vec<Block::Extrinsic>,
        block_number: NumberFor<Block>,
    ) {
        extrinsics.into_iter().for_each(|e| {
            if let Err(e) = Self::apply_extrinsic(e) {
                let err: &'static str = e.into();
                panic!("{}", err)
            }
        });

        // post-extrinsics book-keeping
        <frame_system::Pallet<System>>::note_finished_extrinsics();

        Self::idle_and_finalize_hook(block_number);
    }

    /// Finalize the block - it is up the caller to ensure that all header fields are valid
    /// except state-root.
    pub fn finalize_block() -> System::Header {
        sp_io::init_tracing();
        sp_tracing::enter_span!(sp_tracing::Level::TRACE, "finalize_block");
        <frame_system::Pallet<System>>::note_finished_extrinsics();
        let block_number = <frame_system::Pallet<System>>::block_number();

        Self::idle_and_finalize_hook(block_number);

        <frame_system::Pallet<System>>::finalize()
    }

    fn idle_and_finalize_hook(block_number: NumberFor<Block>) {
        let weight = <frame_system::Pallet<System>>::block_weight();
        let max_weight = <System::BlockWeights as frame_support::traits::Get<_>>::get().max_block;
        let remaining_weight = max_weight.saturating_sub(weight.total());

        if remaining_weight > 0 {
            let used_weight = <AllPalletsWithSystem as OnIdle<System::BlockNumber>>::on_idle(
                block_number,
                remaining_weight,
            );
            <frame_system::Pallet<System>>::register_extra_weight_unchecked(
                used_weight,
                DispatchClass::Mandatory,
            );
        }

        <AllPalletsWithSystem as OnFinalize<System::BlockNumber>>::on_finalize(block_number);
    }

    /// Apply extrinsic outside of the block execution function.
    ///
    /// This doesn't attempt to validate anything regarding the block, but it builds a list of uxt
    /// hashes.
    pub fn apply_extrinsic(uxt: Block::Extrinsic) -> ApplyExtrinsicResult {
        sp_io::init_tracing();
        let encoded = uxt.encode();
        let encoded_len = encoded.len();
        sp_tracing::enter_span!(sp_tracing::info_span!("apply_extrinsic",
				ext=?sp_core::hexdisplay::HexDisplay::from(&encoded)));
        // Verify that the signature is good.
        let xt = uxt.check(&Default::default())?;

        // We don't need to make sure to `note_extrinsic` only after we know it's going to be
        // executed to prevent it from leaking in storage since at this point, it will either
        // execute or panic (and revert storage changes).
        <frame_system::Pallet<System>>::note_extrinsic(encoded);

        // AUDIT: Under no circumstances may this function panic from here onwards.

        // Decode parameters and dispatch
        let dispatch_info = xt.get_dispatch_info();
        let r = Applyable::apply::<UnsignedValidator>(xt, &dispatch_info, encoded_len)?;

        <frame_system::Pallet<System>>::note_applied_extrinsic(&r, dispatch_info);

        Ok(r.map(|_| ()).map_err(|e| e.error))
    }

    fn final_checks(header: &System::Header) {
        sp_tracing::enter_span!(sp_tracing::Level::TRACE, "final_checks");
        // remove temporaries
        let new_header = <frame_system::Pallet<System>>::finalize();

        // check digest
        assert_eq!(
            header.digest().logs().len(),
            new_header.digest().logs().len(),
            "Number of digest items must match that calculated."
        );
        let items_zip = header.digest().logs().iter().zip(new_header.digest().logs().iter());
        for (header_item, computed_item) in items_zip {
            header_item.check_equal(computed_item);
            assert!(header_item == computed_item, "Digest item must match that calculated.");
        }

        // check storage root.
        let storage_root = new_header.state_root();
        header.state_root().check_equal(storage_root);
        assert!(header.state_root() == storage_root, "Storage root must match that calculated.");

        assert!(
            header.extrinsics_root() == new_header.extrinsics_root(),
            "Transaction trie root must be valid.",
        );
    }

    /// Check a given signed transaction for validity. This doesn't execute any
    /// side-effects; it merely checks whether the transaction would panic if it were included or
    /// not.
    ///
    /// Changes made to storage should be discarded.
    pub fn validate_transaction(
        source: TransactionSource,
        uxt: Block::Extrinsic,
        block_hash: Block::Hash,
    ) -> TransactionValidity {
        sp_io::init_tracing();
        use sp_tracing::{enter_span, within_span};

        <frame_system::Pallet<System>>::initialize(
            &(frame_system::Pallet::<System>::block_number() + One::one()),
            &block_hash,
            &Default::default(),
        );

        enter_span! { sp_tracing::Level::TRACE, "validate_transaction" }
        ;

        let encoded_len = within_span! { sp_tracing::Level::TRACE, "using_encoded";
			uxt.using_encoded(|d| d.len())
		};

        let xt = within_span! { sp_tracing::Level::TRACE, "check";
			uxt.check(&Default::default())
		}?;

        let dispatch_info = within_span! { sp_tracing::Level::TRACE, "dispatch_info";
			xt.get_dispatch_info()
		};

        within_span! {
			sp_tracing::Level::TRACE, "validate";
			xt.validate::<UnsignedValidator>(source, &dispatch_info, encoded_len)
		}
    }

    /// Start an offchain worker and generate extrinsics.
    pub fn offchain_worker(header: &System::Header) {
        sp_io::init_tracing();
        // We need to keep events available for offchain workers,
        // hence we initialize the block manually.
        // OffchainWorker RuntimeApi should skip initialization.
        let digests = header.digest().clone();

        <frame_system::Pallet<System>>::initialize(header.number(), header.parent_hash(), &digests);

        // Frame system only inserts the parent hash into the block hashes as normally we don't know
        // the hash for the header before. However, here we are aware of the hash and we can add it
        // as well.
        frame_system::BlockHash::<System>::insert(header.number(), header.hash());

        <AllPalletsWithSystem as OffchainWorker<System::BlockNumber>>::offchain_worker(
            *header.number(),
        )
    }
}
```

### impl<> for xxx 结构体/枚举体+trait：实现接口定义的方法

> impl <trait_name> for <struct/enum name>

```rust
pub trait Summary {
    fn summarize(&self) -> String;
}

pub struct NewsArticle {
    pub headline: String,
    pub location: String,
    pub author: String,
    pub content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.headline, self.author, self.location)
    }
}
```

#### 示例一：实现trait中定义的方法

- [Rust之PhantomData - 简书](https://www.jianshu.com/p/0d60c148c0c0)
- [`type` alias vs `use` - help - The Rust Programming Language Forum](https://users.rust-lang.org/t/type-alias-vs-use/7486)
- where与impl语法的对比：
  - [where可以用于更复杂的情况, 如关联类型](marginnote3app://note/8974BCC4-5036-4051-913A-287D6C6A56A5)
  - [关联类型只能使用where子句](marginnote3app://note/E1B86A91-9D49-4CC5-9344-CAEB316EAC41)

> substrate/frame/executive/src/lib.rs

下列trait限定的意思：

1. 为Executive结构体实现ExecuteBlock这个trait的方法
2. for Executive<...>：Executive本身是个结构体，用到了这些类型
3. impl<...>：这些类型分别有哪些trait限定，要用到关联类型限定的，就放在where子句中
4. where子句：主要先约束好关联类型Block::Extrinsic，给后面的使用
5. 总结impl与where子句：这里将简单情况放在impl中，将复杂的关联类型限定放在where子句中。

```rust
/// Something that can execute a given block.
///
/// Executing a block means that all extrinsics in a given block will be executed and the resulting
/// header will be checked against the header of the given block.
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

pub type CheckedOf<E, C> = <E as Checkable<C>>::Checked;
pub type CallOf<E, C> = <CheckedOf<E, C> as Applyable>::Call;
pub type OriginOf<E, C> = <CallOf<E, C> as Dispatchable>::Origin;

pub struct Executive<
	System,
	Block,
	Context,
	UnsignedValidator,
	AllPalletsWithSystem,
	OnRuntimeUpgrade = (),
>(
	PhantomData<(
		System,
		Block,
		Context,
		UnsignedValidator,
		AllPalletsWithSystem,
		OnRuntimeUpgrade,
	)>,
);


impl<
    System: frame_system::Config + EnsureInherentsAreFirst<Block>,
    Block: traits::Block<Header=System::Header, Hash=System::Hash>,
    Context: Default,
    UnsignedValidator,
    AllPalletsWithSystem: OnRuntimeUpgrade
    + OnInitialize<System::BlockNumber>
    + OnIdle<System::BlockNumber>
    + OnFinalize<System::BlockNumber>
    + OffchainWorker<System::BlockNumber>,
    COnRuntimeUpgrade: OnRuntimeUpgrade,
> ExecuteBlock<Block>
for Executive<System, Block, Context, UnsignedValidator, AllPalletsWithSystem, COnRuntimeUpgrade>
    where
        Block::Extrinsic: Checkable<Context> + Codec,
        CheckedOf<Block::Extrinsic, Context>: Applyable + GetDispatchInfo,
        CallOf<Block::Extrinsic, Context>: Dispatchable<Info=DispatchInfo, PostInfo=PostDispatchInfo>,
        OriginOf<Block::Extrinsic, Context>: From<Option<System::AccountId>>,
        UnsignedValidator: ValidateUnsigned<Call=CallOf<Block::Extrinsic, Context>>,
{
    fn execute_block(block: Block) {
        Executive::<
            System,
            Block,
            Context,
            UnsignedValidator,
            AllPalletsWithSystem,
            COnRuntimeUpgrade,
        >::execute_block(block);
    }
}
```

## Rust面向对象

> Struct/Enum+Trait、Reusable、Encapsulation、Inheritance

- [Characteristics of Object-Oriented Languages - The Rust Programming Language](https://doc.rust-lang.org/book/ch17-01-what-is-oo.html)
- [Implementing an Object-Oriented Design Pattern - The Rust Programming Language](https://doc.rust-lang.org/book/ch17-03-oo-design-patterns.html)

> Object-oriented programs are made up of objects. An object packages both data and the procedures that operate on that
> data. The procedures are typically called methods or operations.

Using this definition, Rust is object-oriented: structs and enums have data, and impl blocks provide methods on structs
and enums. Even though structs and enums with methods aren’t called objects, they provide the same functionality,
according to the Gang of Four’s definition of objects.

### 注意：可以使用图表，对比python和rust的对应面向对象特性实现方式

#### 属性方法

#### 静态方法

#### 实例方法

#### 类方法

### Encapsulation

pub(crate/super) keywords

- [Modules Cheat Sheet](https://doc.rust-lang.org/book/ch07-02-defining-modules-to-control-scope-and-privacy.html#modules-cheat-sheet)

#### Start from the crate root

#### Declaring modules

#### Declaring submodules

mod keyword

#### Paths to code in modules

#### Private vs public

#### The use keyword

### Inheritance

> If a language must have inheritance to be an object-oriented language, then Rust is not one. There is no way to define
> a struct that inherits the parent struct’s fields and method implementations without using a macro.

You would choose inheritance for two main reasons.

#### Reuse

One is for reuse of code: you can implement particular behavior for one type, and inheritance enables you to reuse that
implementation for a different type. You can do this in a limited way in Rust code using default trait method
implementations

#### Polymorphism

The other reason to use inheritance relates to the type system: to enable a child type to be used in the same places as
the parent type. This is also called polymorphism (多态性) , which means that you can substitute multiple objects for each
other at runtime if they share certain characteristics.

> Polymorphism: code that can work with data of multiple types

Rust instead uses generics to abstract over different possible types and trait bounds to impose constraints on what
those types must provide. This is sometimes called **bounded parametric polymorphism** .

## 六、回顾trait，联系上生命周期

- [rust权威指南-trait定义共享行为](marginnote3app://note/133A41C4-ADA0-4101-B280-BCD4D3DB8014)

借助于trait和trait约束,我们可以在使用泛型参数来消除重复代码的同时,向编译器指明自己希望泛型拥有的功能。而编译器则可以利用这些trait约束信息来确保代码中使用的具体类型提供了正确的行为。在动态语言中,尝试调用一个类型没有实现的方法会导致在运行时出现错误。但是,Rust将这些错误出现的时期转移到了编译期,并迫使我们在运行代码之前修复问题。我们无须编写那些用于在运行时检查行为的代码,因为这些工作已经在编译期完成了。这一机制在保留泛型灵活性的同时提升了代码的性能。

生命周期是另外一种你已经接触过的泛型。普通泛型可以确保类型拥有期望的行为,与之不同的是,生命周期能够确保引用在我们的使用过程中一直有效
