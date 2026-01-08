       NoSQL Analysis: MongoDB for FlexiMart Product Catalog

           Section A: Limitations of RDBMS

Relational databases like MySQL are well suited for structured, tabular data, but they struggle when handling highly diverse product catalogs. For example, laptops may require attributes such as RAM, processor, and storage, while shoes need size, color, and material. In an RDBMS, this would require frequent schema changes or multiple specialized tables, leading to complexity and rigidity. Additionally, storing customer reviews is difficult because reviews are naturally nested data (user, rating, comment, date). In a relational model, reviews must be stored in a separate table and joined back, which increases query complexity and reduces performance. As FlexiMart expands to include more product types, the relational schema would become harder to maintain, requiring constant schema migrations and risking anomalies. Thus, RDBMS is not flexible enough for dynamic product catalogs with heterogeneous attributes and embedded reviews.

               

           Section B: Benefits of MongoDB

MongoDB, a document oriented NoSQL database, solves these challenges by offering a flexible schema. Each product can be stored as a JSON     like document, allowing attributes to vary across products without requiring schema changes. For example, laptops can include RAM and processor fields, while shoes can include size and color fields, all within the same collection. Reviews can be embedded directly inside product documents as arrays of sub     documents, making it easy to query products along with their reviews in a single operation. MongoDB also supports horizontal scalability through sharding, enabling FlexiMart to handle large volumes of product and review data efficiently. Its flexible document model aligns naturally with the diverse product catalog, reducing the need for complex joins and schema migrations. This makes MongoDB ideal for storing heterogeneous product data and customer feedback.

               

           Section C: Trade    

While MongoDB offers flexibility, it comes with trade     offs compared to MySQL. First, MongoDB does not enforce strict ACID transactions across multiple documents by default, which can lead to consistency issues in complex financial operations. Second, relational databases are better suited for structured analytical queries, such as aggregating sales trends across normalized tables. MongoDB’s aggregation framework is powerful but less optimized for complex joins. Therefore, while MongoDB is excellent for product catalogs and reviews, MySQL remains more reliable for transactional consistency and analytical workloads. A hybrid approach, using both systems, can balance flexibility and reliability.

