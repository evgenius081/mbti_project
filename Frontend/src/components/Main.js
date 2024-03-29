import React from "react"

import styles from "./Main.module.css"
import {Link} from "react-router-dom";
export function Main(){
    return (
        <>
            <header className={styles.header}>
                <section className={styles.header_description}>
                    <h1 className={styles.h1}>Let's learn ourselves <span className="accent">better</span></h1>
                    <p>Basing on your <span className="accent">Reddit</span> activity and armed with <span className="accent">AI</span>
                        , we can help you to understand your personality better.</p>
                    <Link to={"/about"}>About us</Link>
                </section>
                <section className={styles.header_types}>
                    <article className={styles.header_section_article}>
                        <img src={"/img/2.svg"} alt={"extroversion and introversion"}/>
                        <p className={styles.eitypes_first_type_option}>Extroversion</p>
                        <p className={styles.eitypes_second_type_option}>Introversion</p>
                    </article>
                    <article className={styles.header_section_article}>
                        <img src={"/img/1.svg"} alt={"sensing and intuition"}/>
                        <p className={styles.sitypes_first_type_option}>Sensing</p>
                        <p className={styles.sitypes_second_type_option}>iNtuition</p>
                    </article>
                    <article className={styles.header_section_article}>
                        <img src={"/img/4.svg"} alt={"thinking and feeling"}/>
                        <p className={styles.tftypes_first_type_option}>Thinking</p>
                        <p className={styles.tftypes_second_type_option}>Feeling</p>
                    </article>
                    <article className={styles.header_section_article}>
                        <img src={"/img/3.svg"} alt={"judging and perceiving"}/>
                        <p className={styles.jptypes_first_type_option}>Judging</p>
                        <p className={styles.jptypes_second_type_option}>Perceiving</p>
                    </article>
                </section>
            </header>
        </>
    )
}