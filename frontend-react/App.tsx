import { useState } from "react";
import MainLanding from "./components/MainLanding";
import AuthPage from "./components/AuthPage";
// import { MainDashboard } from "./components/MainDashboard";
export default function App() {
  const [currentPage, setCurrentPage] = useState<
    "landing" | "auth"
  >("landing");

  const handleGetStarted = () => {
    setCurrentPage("auth");
  };

  const handleBackToHome = () => {
    setCurrentPage("landing");
  };

  return (
    <div className="min-h-screen">
      {currentPage === "landing" ? (
        <MainLanding onGetStarted={handleGetStarted} />
      ) : (
        <AuthPage onBack={handleBackToHome} />
      )}
    </div>
  );
}
