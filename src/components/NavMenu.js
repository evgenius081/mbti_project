import React from 'react';
import { Link } from 'react-router-dom'

import styles from "./NavMenu.module.css"

export function NavMenu(){

    return (
        <nav className={styles.nav}>
            <div className={styles.logo}>
                <Link to="/" className={styles.logo_a}>mbti<span className={"accent"}>fy</span></Link>
            </div>
            <Link to={"types/test"} className={styles.test_button}>Try for free</Link>
        </nav>
    );
}
