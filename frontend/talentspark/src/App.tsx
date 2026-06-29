import Welcome from "./components/Welcome";
import NavBar from "./components/NavBar";
import CompanyCard from "./components/CompanyCard";
import JobCard from "./components/JobCard";
import Footer from "./components/Footer";

function App(){
  return(
    <>
    <NavBar />
    <Welcome />
    <br />
    <CompanyCard />
    <JobCard />
    <Footer />
    </>
  )
}

export default App