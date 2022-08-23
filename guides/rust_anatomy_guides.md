# rust项目解剖图绘制指南

## crate处理

根据crate找到相关的crate，这是最顶级的层级。

- 这里的crate指的是特定的目录结构, cargo.toml里面可能含有本地的src同级目录crate，那个算作单独的crate
- 一个crate看作最顶级的package

## mod处理

- 一个mod对应二级package, 它们就是各个class/struct/enum/trait的容器
- 内部嵌套mod依次对应下级package

## struct/enum/trait处理
这些就是对应的class级别

