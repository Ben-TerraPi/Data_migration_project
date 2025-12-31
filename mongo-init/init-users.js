db = db.getSiblingDB('datasolutech');

db.createUser({
  user: process.env.MONGO_USER,
  pwd: process.env.MONGO_USER_PASSWORD,
  roles: [
    { role: "read", db: "datasolutech" }
  ]
});