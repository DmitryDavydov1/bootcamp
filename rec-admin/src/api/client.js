import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

const createFormData = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return formData;
};

export const uploadTitleFile = (file) => {
  return api.post("/api/data/upload-title", createFormData(file));
};

export const uploadCtrFile = (file) => {
  return api.post("/api/data/upload-ctr", createFormData(file));
};

export const generateReport = () => {
  return api.post("/api/recommendations/generate");
};

export const getCurrentTop = () => {
  return api.get("/api/recommendations/current-top");
};

export const saveCurrentTop = (data) => {
  return api.post("/api/recommendations/current-top", data);
};