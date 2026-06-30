import type {job} from "./job";
interface Company{
    id:number;
    name:string;
    email:string;
    phone:string;
    location:string;
    jobs:job[];
}
export type {Company}