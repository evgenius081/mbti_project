import React, {useContext, useEffect} from "react"
import {useParams, useNavigate} from "react-router-dom";
import styles from "./TypeDescription.module.css"
import {Context} from "../context";
import {typeDesciptions} from "./typeDescriptions";


export function TypeDescription(){
    let {type} = useParams()
    let navigate = useNavigate()
    const {mbtiTypes} = useContext(Context);

    let type_percents = Object.values(mbtiTypes).map(value => Object.values(value))
        .map(value => (value[1] / (value[0] + value[1])) * 50)

    useEffect(() => {
        const types = ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP",
            "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]
        if (!types.includes(type.toUpperCase())){
            navigate("/not-found")
        }
    }, [type, navigate])

    return (
        <main className={styles.main}>
            {mbtiTypes["IE"][0] === 0 && mbtiTypes["IE"][1] === 0 ? null : (
                <>
            <h1 className={styles.h1}>Your MBTI type is <span className={"accent"}>{type.toUpperCase()}</span></h1>
            <section className={styles.letters_procents}>
                <article className={styles.letter_procents}>
                    <div className={styles.letter_names}>
                        <p className={styles.letter_name}>Introversion</p>
                        <p className={styles.letter_name}>Extroversion</p>
                    </div>
                    <div className={styles.letter_bar_wrapper}>
                        <div style={{left:type_percents[0]+"%"}}
                             className={styles.ei_letter_bar}>
                        </div>
                    </div>
                </article>
                <article className={styles.letter_procents}>
                    <div className={styles.letter_names}>
                        <p className={styles.letter_name}>iNtuition</p>
                        <p className={styles.letter_name}>Sensing</p>
                    </div>
                    <div className={styles.letter_bar_wrapper}>
                        <div style={{left:type_percents[2]+"%"}}
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
                        <div style={{left:type_percents[3]+"%"}}
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
                        <div style={{left:type_percents[1]+"%"}}
                             className={styles.jp_letter_bar}></div>
                    </div>
                </article>
            </section>
                </>
    )}
            <section>
                {typeDesciptions[type]}
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