db = db.getSiblingDB('datasolutech');

db.createUser({
  user: "user",
  pwd: "user",
  roles: [
    { role: "read", db: "datasolutech" }
  ]
});