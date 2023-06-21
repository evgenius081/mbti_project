import { Link } from 'react-router-dom';
import React from 'react'

export function InternalError(props) {
    return (
        <section className="error">
        <div className="error-internal-header error-header">
            <h1>Error occurred</h1>
        </div>
        <div className="error-text">
            <p>Internal server error occurred. If this situation continues, please feel free to contact <Link to="mailto:s187721@student.pg.edu.pl">us</Link>.</p>
            <p><br />Proceed to <Link to="/">main</Link></p>
            </div>
    </section>
    )
}