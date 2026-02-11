import './DashboardPage.css';
import React from 'react';

type profileData = {
    id: number;
    username: string;
    email: string;
    date_joined: string;    
}

type categoryData = {
    id: number;
    name: string;
    type: "INCOME" | "EXPENSE" | "SPENDING";
}

type transactionData = {
    id: number;
    amount: number;
    category: categoryData; //nested category object(id, name, type)
    date: string;
    description: string;
}

type financeSummary ={
    
}
export default function DashboardPage() {
    return (
        <div className="dashboard-page">
            <h1>Welcome to the Dashboard</h1>
            <p>This is your main dashboard where you can manage your account and view important information.</p>
        </div>
    );
}