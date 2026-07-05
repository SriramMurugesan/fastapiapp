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
        <div className="page-container">
            <h2>Companies</h2>
            <div className="grid-layout">
                {companies.map((company) => (
                    <div key={company.id} className="card">
                        {editCompanyId === company.id ? (
                            <>
                                <input type="text" value={editform.name} onChange={(e)=>setEditform({...editform,name:e.target.value})} placeholder="Name" />
                                <input type="text" value={editform.email} onChange={(e)=>setEditform({...editform,email:e.target.value})} placeholder="Email" />
                                <input type="text" value={editform.phone} onChange={(e)=>setEditform({...editform,phone:e.target.value})} placeholder="Phone" />
                                <input type="text" value={editform.location} onChange={(e)=>setEditform({...editform,location:e.target.value})} placeholder="Location" />
                                <div className="action-buttons">
                                    <button onClick={handleSave}>Save</button>
                                    <button onClick={handlecancel}>Cancel</button>
                                </div>
                            </>
                        ):
                        <>
                            <h3>{company.name}</h3>
                            <p><strong>Email:</strong> {company.email}</p>
                            <p><strong>Phone:</strong> {company.phone}</p>
                            <p><strong>Location:</strong> {company.location}</p>
                            <p><strong>Jobs:</strong> {jobs.filter(j => j.company_id === company.id).length} opening{jobs.filter(j => j.company_id === company.id).length === 1 ? '' : 's'}</p>
                            <div className="action-buttons">
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
                            </div>
                        </>}
                    </div>
                ))}
            </div>

            <div style={{ marginTop: '3rem' }}>
                <h2>Add Company</h2>
                <div className="grid-layout" style={{ maxWidth: '600px', gridTemplateColumns: '1fr' }}>
                    <div className="card">
                        <input type="text" value={addform.name} onChange={(e)=>setAddform({...addform,name:e.target.value})} placeholder="Name" />
                        <input type="text" value={addform.email} onChange={(e)=>setAddform({...addform,email:e.target.value})} placeholder="Email" />
                        <input type="text" value={addform.phone} onChange={(e)=>setAddform({...addform,phone:e.target.value})} placeholder="Phone" />
                        <input type="text" value={addform.location} onChange={(e)=>setAddform({...addform,location:e.target.value})} placeholder="Location" />
                        <button onClick={handleAdd} style={{ width: '100%' }}>Add Company</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default CompanyCard