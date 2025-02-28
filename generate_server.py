import json

def generate_server(json_file, output_file="server.js"):
    with open(json_file, "r") as f:
        data = json.load(f)

    nodes = {node["id"]: node for node in data["nodes"]}
    routes = []
    middlewares = {"cors": "", "auth": "", "admin": ""}

    # Loop through nodes to generate middleware and routes
    for node in nodes.values():
        props = node.get("properties", {})

        
        node_type = props.get("type", "route")  

        # CORS Middleware
        if node_type == "middleware" and "allowed_origins" in props:
            middlewares["cors"] = f'app.use(cors({{"origin": {props["allowed_origins"]}}}));'

        # Authentication Middleware
        if node_type == "middleware" and "auth_required" in props:
            middlewares["auth"] = '''const authMiddleware = (req, res, next) => {
    if (!req.headers.authorization) {
        return res.status(401).json({ message: "Unauthorized" });
    }
    next();
};'''

        
        if node_type == "middleware" and "admin_required" in props:
            middlewares["admin"] = '''const adminMiddleware = (req, res, next) => {
    if (req.headers.authorization !== "admin-token") {
        return res.status(403).json({ message: "Forbidden" });
    }
    next();
};'''

        # Generate Routes
        if "endpoint" in props and "method" in props:
            route = f'app.{props["method"].lower()}("{props["endpoint"]}", '
            if props.get("admin_required"):
                route += "authMiddleware, adminMiddleware, "
            elif props.get("auth_required"):
                route += "authMiddleware, "
            route += f"(req, res) => res.json({{ message: \"{node['name']}\" }}));"
            routes.append(route)

    # Generate final server.js content
    server_code = f'''const express = require("express");
const cors = require("cors");
const app = express();
app.use(express.json());

{middlewares["cors"]}

{middlewares["auth"]}

{middlewares["admin"]}

{"\n".join(routes)}

app.listen(3000, () => console.log("Server running on port 3000"));'''

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(server_code)

    print(f" Server generated successfully in {output_file}")


if __name__ == "__main__":
    generate_server("input.json")
