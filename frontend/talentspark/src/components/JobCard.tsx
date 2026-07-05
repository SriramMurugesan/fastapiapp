import type {Job} from "../types/job";
import type {Company} from "../types/company";

import {useState} from "react";

type Props = {
    jobs:Job[];
    companies:Company[];
    onEdit: (job:Job)=>void;
    onDelete: (id:number)=>void;
    onAdd: (job:Job)=>void;
}

function JobCard({
    jobs,companies,onEdit,onDelete,onAdd}:Props){
        const [editJobId, setEditJobId] = useState<number | null>(null);
        const [addform,setAddform] = useState<Job>({
            id:0,
            title:"",
            description:"",
            salary:"",
            company_id:0
        });
        const [editform,setEditform] = useState<Job>({
            id:0,
            title:"",
            description:"",
            salary:"",
            company_id:0
        });
        const handleAdd = () => {
            onAdd(addform);
            setAddform({
                id:0,
                title:"",
                description:"",
                salary:"",
                company_id:0
            })
        }
        const handleSave = () => {
            onEdit(editform);
            setEditJobId(null);
            setEditform({
                id:0,
                title:"",
                description:"",
                salary:"",
                company_id:0
            })
        }
        const handlecancel = () => {
            setEditJobId(null);
            setEditform({
                id:0,
                title:"",
                description:"",
                salary:"",
                company_id:0
            })
        }

    return(
        <div className="page-container" style={{ marginTop: '4rem' }}>
            <h2>Jobs</h2>
            <div className="grid-layout">
                {jobs.map((job) => (
                    <div key={job.id} className="card">
                        {editJobId === job.id ? (
                            <>
                                <input type="text" value={editform.title} onChange={(e)=>setEditform({...editform,title:e.target.value})} placeholder="Title" />
                                <input type="text" value={editform.description} onChange={(e)=>setEditform({...editform,description:e.target.value})} placeholder="Description" />
                                <input type="text" value={editform.salary} onChange={(e)=>setEditform({...editform,salary:e.target.value})} placeholder="Salary" />
                                <input type="number" value={editform.company_id} onChange={(e)=>setEditform({...editform,company_id:Number(e.target.value)})} placeholder="Company ID" />
                                <div className="action-buttons">
                                    <button onClick={handleSave}>Save</button>
                                    <button onClick={handlecancel}>Cancel</button>
                                </div>
                            </>
                        ):
                        <>
                            <h3>{job.title}</h3>
                            <p><strong>Description:</strong> {job.description}</p>
                            <p><strong>Salary:</strong> {job.salary}</p>
                            <p><strong>Company:</strong> {companies.find(c => c.id === job.company_id)?.name || job.company_id}</p>
                            <div className="action-buttons">
                                <button
                                    onClick={() => {
                                        setEditJobId(job.id);
                                        setEditform({
                                            id: job.id,
                                            title: job.title,
                                            description: job.description,
                                            salary: job.salary,
                                            company_id: job.company_id,
                                        });
                                    }}
                                >Edit</button>
                                <button onClick={() => onDelete(job.id)}>Delete</button>
                            </div>
                        </>}
                    </div>
                ))}
            </div>

            <div style={{ marginTop: '3rem' }}>
                <h2>Add Job</h2>
                <div className="grid-layout" style={{ maxWidth: '600px', gridTemplateColumns: '1fr' }}>
                    <div className="card">
                        <input type="text" value={addform.title} onChange={(e)=>setAddform({...addform,title:e.target.value})} placeholder="Title" />
                        <input type="text" value={addform.description} onChange={(e)=>setAddform({...addform,description:e.target.value})} placeholder="Description" />
                        <input type="text" value={addform.salary} onChange={(e)=>setAddform({...addform,salary:e.target.value})} placeholder="Salary" />
                        <input type="number" value={addform.company_id} onChange={(e)=>setAddform({...addform,company_id:Number(e.target.value)})} placeholder="Company ID" />
                        <button onClick={handleAdd} style={{ width: '100%' }}>Add Job</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default JobCard