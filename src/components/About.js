import React from "react"

import styles from "./About.module.css"

export function About(){

    return (
        <main>
            <section className={styles.team_header}>
                <h2>We are <span className={"accent"}>Capibara</span> team</h2>
            </section>
            <section className={styles.team_members}>
                <article className={styles.team_member}>
                    <img src={"img/yauheni.png"} alt={"Yauheni"}/>
                    <div>
                        <p>Yauheni Hulevich</p>
                    </div>
                </article>
                <article className={styles.team_member}>
                    <img src={"img/danila.jpg"} alt={"Danila"} />
                    <div>
                        <p>Danila Rubleuski</p>
                    </div>
                </article>
                <article className={styles.team_member}>
                    <img src={"img/marharyta.jpg"} alt={"Marharyta"}/>
                    <div>
                        <p>Marharyta Karnilava</p>
                    </div>
                </article>
                <article className={styles.team_member}>
                    <img src={"img/capibara.jpg"} alt={"capibara"}/>
                    <div>
                        <p>Capibara Capibara</p>
                    </div>
                </article>
            </section>
        </main>
    )
}