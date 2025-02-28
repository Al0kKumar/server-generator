const express = require("express");
const cors = require("cors");
const app = express();
app.use(express.json());

app.use(cors({"origin": ['http://example.com']}));

const authMiddleware = (req, res, next) => {
    if (!req.headers.authorization) {
        return res.status(401).json({ message: "Unauthorized" });
    }
    next();
};



app.post("/login", (req, res) => res.json({ message: "Login Route" }));
app.get("/admin", authMiddleware, adminMiddleware, (req, res) => res.json({ message: "Admin Route" }));

app.listen(3000, () => console.log("Server running on port 3000"));