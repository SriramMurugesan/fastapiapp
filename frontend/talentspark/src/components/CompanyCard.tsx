import type {Company} from "../types/company";
import type {Job} from "../types/job";
import {useState} from "react";

type Props = {
    companies:Company[];
    jobs:Job[];
    onEdit: (company:Company)=>void;
    onDelete: (id:number)=>void;
    onAdd: (company:Company)=>void;
}


function CompanyCard({
    companies,jobs,onAdd,onEdit,onDelete}:Props){
    const [editCompanyId, setEditCompanyId] = useState<number | null>(null);
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
        onAdd(addform);
        setAddform({
            id:0,
            name:"",
            email:"",
            phone:"",
            location:"",
            jobs:[]
        })
    }
    const handleSave = () => {
        onEdit(editform);
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
                    <input type="text" value={editform.name} onChange={(e)=>setEditform({...editform,name:e.target.value})} placeholder="Name" />
                    <input type="text" value={editform.email} onChange={(e)=>setEditform({...editform,email:e.target.value})} placeholder="Email" />
                    <input type="text" value={editform.phone} onChange={(e)=>setEditform({...editform,phone:e.target.value})} placeholder="Phone" />
                    <input type="text" value={editform.location} onChange={(e)=>setEditform({...editform,location:e.target.value})} placeholder="Location" />
                    <button onClick={handleSave}>Save</button>
                    <button onClick={handlecancel}>Cancel</button>
                    </>
                    ):
                    <>
                    <h1>{company.name}</h1>
                    <p>Email: {company.email}</p>
                    <p>Phone: {company.phone}</p>
                    <p>Location: {company.location}</p>
                    <p>Jobs: {jobs.filter(j => j.company_id === company.id).length} opening{jobs.filter(j => j.company_id === company.id).length === 1 ? '' : 's'}</p>
                    <button
                        onClick={() => {
                            setEditCompanyId(company.id);
                            setEditform({
                                id: company.id,
                                name: company.name,
                                email: company.email,
                                phone: company.phone,
                                location: company.location,
                                jobs: company.jobs,
                            });
                        }}
                    >Edit</button>
                    <button onClick={() => onDelete(company.id)}>Delete</button>
                    </>}
                    <hr></hr>
                </div>
            ))}
            <h2>Add Company</h2>
            <input type="text" value={addform.name} onChange={(e)=>setAddform({...addform,name:e.target.value})} placeholder="Name" />
            <input type="text" value={addform.email} onChange={(e)=>setAddform({...addform,email:e.target.value})} placeholder="Email" />
            <input type="text" value={addform.phone} onChange={(e)=>setAddform({...addform,phone:e.target.value})} placeholder="Phone" />
            <input type="text" value={addform.location} onChange={(e)=>setAddform({...addform,location:e.target.value})} placeholder="Location" />
            <button onClick={handleAdd}>Add</button>
        </div>
    )
}

export default CompanyCard