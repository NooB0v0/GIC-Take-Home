import { Routes, Route, useNavigate } from "react-router-dom";
import { Layout, Menu, theme } from "antd";
import { CoffeeOutlined } from "@ant-design/icons";
import CafeList from "./pages/Cafes/CafeList";
import CafeForm from "./pages/Cafes/CafeForm";
import EmployeeList from "./pages/Employees/EmployeeList";
import EmployeeForm from "./pages/Employees/EmployeeForm";

const { Header, Content, Footer } = Layout;

const navItems = [
  { key: "/cafes", label: "Cafes", icon: <CoffeeOutlined /> },
  { key: "/employees", label: "Employees", icon: <CoffeeOutlined /> },
];

function App() {
  const navigate = useNavigate();
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  return (
      <Layout style={{ minHeight: "100vh", width: "100%" }}>
        <Header
          style={{
            display: "flex",
            alignItems: "center",
            background: colorBgContainer,
          }}
        >
          <div
            style={{
              color: "#543D3F",
              fontWeight: "bold",
              fontSize: "20px",
              marginRight: "50px",
            }}
          >
            ☕ Cafe Manager
          </div>
          <Menu
            theme="light"
            mode="horizontal"
            defaultSelectedKeys={["/cafes"]}
            items={navItems}
            style={{ flex: 1, minWidth: 0 }}
            // Use navigation to update the URL
            onSelect={({ key }) => navigate(key)}
          />
        </Header>
        <Content style={{ padding: "24px", minHeight: "80vh" }}>
          <div
            style={{
              background: colorBgContainer,
              padding: 24,
              minHeight: "100%",
              width: "100%",
            }}
          >
            <Routes>
              <Route path="/" element={<CafeList />} />{" "}
              {/* Default to Cafes Page */}
              <Route path="/cafes" element={<CafeList />} />
              <Route path="/employees" element={<EmployeeList />} />
              {/* FUTURE ROUTES: Add/Edit forms will go here */}
              <Route path="/cafes/add" element={<CafeForm />} />
              <Route path="/cafes/edit/:id" element={<CafeForm />} />
              <Route path="/employees/add" element={<EmployeeForm />} />{" "}
              {/* Add New Employee */}
              <Route path="/employees/edit/:id" element={<EmployeeForm />} />{" "}
              {/* Edit Existing Employee */}
            </Routes>
          </div>
        </Content>
        <Footer style={{ textAlign: "center" }}>
         
        </Footer>
      </Layout>
  );
}

export default App;
