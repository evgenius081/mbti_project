import React, {useState} from "react"

import styles from "./Test.module.css"

export function Test(){
    const [userName, setUserName] = useState("")
    const [showPlaceholder, setShowPlaceholder] = useState(true)

    function check(text){
        if (text.length === 0){
            setShowPlaceholder(true)

        }else{
            setShowPlaceholder(false)
        }
        setUserName(text)

    }

    function send(e){
        e.preventDefault()
    }

    return (
        <main>
            <section className={styles.test}>
                <form className={styles.test_form}>
                    <input type={"text"} className={styles.user_name} value={userName}
                           onChange={e => setUserName(e.target.value)}
                           onFocus={() => setShowPlaceholder(false)}
                        onBlur={e => check(e.target.value)}></input>
                    {showPlaceholder ? <p className={styles.placeholder}>Enter <span className={"accent"}>Redditor</span> name</p> : null}
                    <button type={"submit"} className={styles.send} onClick={e => send(e)}>Learn yourself</button>
                </form>
            </section>
        </main>
    )
}