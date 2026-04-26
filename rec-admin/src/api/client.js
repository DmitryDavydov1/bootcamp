import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return api.post("/api/data/upload", formData);
};

export const generateReport = () => {
  return api.post("/api/recommendations/generate");
};