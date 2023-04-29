import React, {useEffect} from "react"
import {useParams, useNavigate} from "react-router-dom";

import styles from "./TypeDescription.module.css"
export function TypeDescription(){
    // const types = ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP",
    //  "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]
    let {type} = useParams()
    let navigate = useNavigate()
    let type_percents_raw = [{"I":20, "E":10}, {"S":3, "N": 16}, {"T": 5, "F":5},
        {"J": 15, "P": 5}]

    let type_percents = type_percents_raw.map(value => Object.values(value))
        .map(value => value[1] / (value[0] + value[1]) * 50)

    console.log(type_percents)

    useEffect(() => {
        const types = ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP",
            "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]
        if (!types.includes(type.toUpperCase())){
            navigate("/not-found")
        }
    }, [type, navigate])

    return (
        <main className={styles.main}>
            <h1 className={styles.h1}>Your MBTI type is <span className={"accent"}>{type.toUpperCase()}</span></h1>
            <section className={styles.letters_procents}>
                <article className={styles.letter_procents}>
                    <div className={styles.letter_names}>
                        <p className={styles.letter_name}>Extroversion</p>
                        <p className={styles.letter_name}>Introversion</p>
                    </div>
                    <div className={styles.letter_bar_wrapper}>
                        <div style={{left:type_percents[0]+"%"}}
                             className={styles.ei_letter_bar}>
                        </div>
                    </div>
                </article>
                <article className={styles.letter_procents}>
                    <div className={styles.letter_names}>
                        <p className={styles.letter_name}>Sensing</p>
                        <p className={styles.letter_name}>iNtuition</p>
                    </div>
                    <div className={styles.letter_bar_wrapper}>
                        <div style={{left:type_percents[1]+"%"}}
                             className={styles.si_letter_bar}>
                        </div>
                    </div>
                </article>
                <article className={styles.letter_procents}>
                    <div className={styles.letter_names}>
                        <p className={styles.letter_name}>Thinking</p>
                        <p className={styles.letter_name}>Feeling</p>
                    </div>
                    <div className={styles.letter_bar_wrapper}>
                        <div style={{left:type_percents[2]+"%"}}
                             className={styles.tf_letter_bar}>
                        </div>
                    </div>
                </article>
                <article className={styles.letter_procents}>
                    <div className={styles.letter_names}>
                        <p className={styles.letter_name}>Judging</p>
                        <p className={styles.letter_name}>Perceiving</p>
                    </div>
                    <div className={styles.letter_bar_wrapper}>
                        <div style={{left:type_percents[3]+"%"}}
                             className={styles.jp_letter_bar}></div>
                    </div>
                </article>
            </section>
            <section>
                <p className={styles.type_description_p}><span className={"accent"}>INFJ</span>s are known for being intuitive, empathetic, and imaginative individuals. They have a deep understanding of other people's emotions and can be incredibly insightful when it comes to understanding complex situations. With their strong sense of purpose and commitment to their values, <span className={"accent"}>INFJ</span>s make great advocates for social justice and can be very effective at inspiring positive change. At the same time, they can be very private and introspective, needing time alone to recharge and reflect on their thoughts and feelings.</p>
            </section>
            <section className={styles.personalities_link}>
                <p className={styles.personalities_link_p}>More at <a
                    href={"https://www.16personalities.com/"+type.toLowerCase()+"-personality"}
                    className={styles.personalities_link_a}>16personalities.com</a>
                </p>
            </section>
        </main>
    )
}