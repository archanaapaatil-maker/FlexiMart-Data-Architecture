 
// MongoDB Operations for FlexiMart Product Catalog

// Operation 1: Load Data 
Import the provided JSON file into collection 'products'
 Run this in terminal: mongoimport --db fleximart --collection products --file products_catalog.json --jsonArray

 Operation 2: Basic Query
 Find all products in "Electronics" category with price less than 50000
db.products.find(
  { category: "Electronics", price: { $lt: 50000 } },
  { name: 1, price: 1, stock: 1 }
);

 Operation 3: Review Analysis
// Find all products that have average rating >= 4.0
db.products.aggregate([
  { $unwind: "$reviews" },
  { $group: { _id: "$name", avgRating: { $avg: "$reviews.rating" } } },
  { $match: { avgRating: { $gte: 4.0 } } }
]);

// Operation 4: Update Operation 
// Add a new review to product "ELEC001"
db.products.updateOne(
  { product_id: "ELEC001" },
  { $push: { reviews: { user_id: "U999", username: "NewUser", rating: 4, comment: "Good value", date: ISODate("2024-04-01") } } }
);
