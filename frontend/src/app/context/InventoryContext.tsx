import React, { createContext, useContext, useState, ReactNode } from "react";
import { loginService } from "../services/auth";

const [token, setToken] = useState<string | null>(null);

const login = async (username: string, password: string) => {
  const data = await loginService(username, password);
  setToken(data.access_token);  // ← stocké en mémoire
};

const logout = () => {
  setToken(null);  // ← effacé
};

export interface Product {
  id: string;
  name: string;
  sku: string;
  category: string;
  quantity: number;
  minStock: number;
  price: number;
  lastUpdated: string;
  supplier: string;
  location: string;
}

interface InventoryContextType {
  products: Product[];
  addProduct: (product: Omit<Product, "id" | "lastUpdated">) => void;
  updateProduct: (id: string, product: Partial<Product>) => void;
  deleteProduct: (id: string) => void;
  getProductById: (id: string) => Product | undefined;
}

const InventoryContext = createContext<InventoryContextType | undefined>(undefined);

const initialProducts: Product[] = [
  {
    id: "1",
    name: "Wireless Mouse",
    sku: "WM-001",
    category: "Electronics",
    quantity: 145,
    minStock: 50,
    price: 29.99,
    lastUpdated: "2026-01-25",
    supplier: "Tech Supplies Inc",
    location: "Warehouse A",
  },
  {
    id: "2",
    name: "Mechanical Keyboard",
    sku: "MK-002",
    category: "Electronics",
    quantity: 32,
    minStock: 40,
    price: 89.99,
    lastUpdated: "2026-01-24",
    supplier: "Tech Supplies Inc",
    location: "Warehouse A",
  },
  {
    id: "3",
    name: "USB-C Cable",
    sku: "UC-003",
    category: "Accessories",
    quantity: 250,
    minStock: 100,
    price: 12.99,
    lastUpdated: "2026-01-26",
    supplier: "Cable World",
    location: "Warehouse B",
  },
  {
    id: "4",
    name: "Laptop Stand",
    sku: "LS-004",
    category: "Furniture",
    quantity: 18,
    minStock: 25,
    price: 45.99,
    lastUpdated: "2026-01-23",
    supplier: "Office Depot",
    location: "Warehouse A",
  },
  {
    id: "5",
    name: "Webcam HD",
    sku: "WC-005",
    category: "Electronics",
    quantity: 67,
    minStock: 30,
    price: 79.99,
    lastUpdated: "2026-01-27",
    supplier: "Tech Supplies Inc",
    location: "Warehouse C",
  },
  {
    id: "6",
    name: "Office Chair",
    sku: "OC-006",
    category: "Furniture",
    quantity: 8,
    minStock: 15,
    price: 199.99,
    lastUpdated: "2026-01-22",
    supplier: "Office Depot",
    location: "Warehouse B",
  },
  {
    id: "7",
    name: "Monitor 27 inch",
    sku: "MN-007",
    category: "Electronics",
    quantity: 42,
    minStock: 20,
    price: 299.99,
    lastUpdated: "2026-01-26",
    supplier: "Display Masters",
    location: "Warehouse A",
  },
  {
    id: "8",
    name: "Desk Lamp",
    sku: "DL-008",
    category: "Lighting",
    quantity: 95,
    minStock: 40,
    price: 34.99,
    lastUpdated: "2026-01-25",
    supplier: "Light House",
    location: "Warehouse C",
  },
];

export function InventoryProvider({ children }: { children: ReactNode }) {
  const [products, setProducts] = useState<Product[]>(initialProducts);

  const addProduct = (productData: Omit<Product, "id" | "lastUpdated">) => {
    const newProduct: Product = {
      ...productData,
      id: Date.now().toString(),
      lastUpdated: new Date().toISOString().split("T")[0],
    };
    setProducts([...products, newProduct]);
  };

  const updateProduct = (id: string, productData: Partial<Product>) => {
    setProducts(
      products.map((product) =>
        product.id === id
          ? {
              ...product,
              ...productData,
              lastUpdated: new Date().toISOString().split("T")[0],
            }
          : product
      )
    );
  };

  const deleteProduct = (id: string) => {
    setProducts(products.filter((product) => product.id !== id));
  };

  const getProductById = (id: string) => {
    return products.find((product) => product.id === id);
  };

  return (
    <InventoryContext.Provider
      value={{
        products,
        addProduct,
        updateProduct,
        deleteProduct,
        getProductById,
      }}
    >
      {children}
    </InventoryContext.Provider>
  );
}

export function useInventory() {
  const context = useContext(InventoryContext);
  if (!context) {
    throw new Error("useInventory must be used within InventoryProvider");
  }
  return context;
}
