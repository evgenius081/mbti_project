import { Link } from 'react-router-dom';
import React from 'react'

export function NotFound() {
    return (
        <section className="error">
        <div className="error-not-found-header error-header">
            <h1>Not found</h1>
        </div>
        <div className="error-text">
            <p>The page you are searching was not found. Try the other one.</p>
            <p><br />Proceed to <Link to="/">main</Link></p>
            </div>
    </section>
    )
}