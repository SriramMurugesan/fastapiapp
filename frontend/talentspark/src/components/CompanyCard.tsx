import type {Company} from "../types/company";
import { getCompany} from "../Services/CompanyService";
import {useState} from "react";

type Props = {
    companies:Company[];
    onedit: (company:Company)=>void;
    ondelete: (id:number)=>void;
    onadd: (company:Company)=>void;
}


function CompanyCard({
    companies,onadd,onedit,ondelete}:Props){
    const [editCompanyId, setEditCompanyId] = useState<number | null>(null);
    const [editcompany, setEditcompany] = useState<Company | null>(null);
    const [addform,setAddform] = useState<Company>({
        id:0,
        name:"",
        email:"",
        phone:"",
        location:"",
        jobs:[]
    });
    const [editform,setEditform] = useState<Company>({
        id:0,
        name:"",
        email:"",
        phone:"",
        location:"",
        jobs:[]
    });
    const handleAdd = () => {
        onadd(addform);
        setAddform({
            id:0,
            name:"",
            email:"",
            phone:"",
            location:"",
            jobs:[]
        })
    }
    const handleEdit = (company:Company) => {
        onedit(company);
        setEditform({
            id:company.id,
            name:company.name,
            email:company.email,
            phone:company.phone,
            location:company.location,
            jobs:[]
        })
    }
    const handleDelete = (id:number) => {
        ondelete(id);
    }
    const handleSave = (id:number) => {
        onedit(editform);
        setEditform({
            id:0,
            name:"",
            email:"",
            phone:"",
            location:"",
            jobs:[]
        })
    } 
    const handlecancel = () => {
        setEditCompanyId(null);
        setEditform({
            id:0,
            name:"",
            email:"",
            phone:"",
            location:"",
            jobs:[]
        })
    } 

    return(
        <div>
            {companies.map((company) => (
                <div key={company.id}>
                    {editCompanyId === company.id ? (
                        <>
                    <input type="text" value={editform.name} onChange={(e)=>setEditform({...editform,name:e.target.value})} />
                    <input type="text" value={editform.email} onChange={(e)=>setEditform({...editform,email:e.target.value})} />
                    <input type="text" value={editform.phone} onChange={(e)=>setEditform({...editform,phone:e.target.value})} />
                    <input type="text" value={editform.location} onChange={(e)=>setEditform({...editform,location:e.target.value})} />
                    <button onClick={() => handleSave(company.id)}>Save</button>
                    <button onClick={handlecancel}>Cancel</button>
                    </>
                    ):
                    <>
                    <h1>{company.name}</h1>
                    <p>Email: {company.email}</p>
                    <p>Phone: {company.phone}</p>
                    <p>Location: {company.location}</p>
                    </>}
                    <button onClick={() => setEditCompanyId(company.id)}>Edit</button>
                    <button onClick={() => ondelete(company.id)}>Delete</button>
                    <hr></hr>
                </div>
            ))}
        </div>
    )
}

export default CompanyCard