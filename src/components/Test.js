import React, {useState, useContext} from "react"
import {useNavigate} from "react-router-dom";

import styles from "./Test.module.css"
import {Context} from "../context";

export function Test(){
    let navigate = useNavigate()
    const {setMbtiTypes} = useContext(Context);
    const [chosenType, setChosenType] = useState("user")
    const [userName, setUserName] = useState("")
    const [text, setText] = useState("")
    const [showNamePlaceholder, setShowNamePlaceholder] = useState(true)
    const [showTextPlaceholder, setShowTextPlaceholder] = useState(true)
    const [buttonStatus, setButtonStatus] = useState("Learn yourself")
    const [disabled, setDisabled] = useState(false)

    function checkUserName(name){
        if (name.length === 0){
            setShowNamePlaceholder(true)

        }else{
            setShowNamePlaceholder(false)
        }
        setUserName(name)
    }

    function checkText(txt){
        if (txt.length === 0){
            setShowTextPlaceholder(true)

        }else{
            setShowTextPlaceholder(false)
        }
        setText(txt)
    }

    async function send(e){
        e.preventDefault()

        setButtonStatus("Loading")
        setDisabled(true)
        console.log("dadwd")

        if (chosenType === "user"){
            await fetch(process.env.REACT_APP_BACKEND_LINK + "/user?username="+userName)
                .then(async (response) => {
                    if (response.ok){
                        let data = await response.json()
                        setMbtiTypes(data)
                        let primaryType = data["IE"][0] > data["IE"][1] ? "i" : "e"
                        primaryType += data["NS"][0] > data["NS"][1] ? "n" : "s"
                        primaryType += data["TF"][0] > data["TF"][1] ? "t" : "f"
                        primaryType += data["JP"][0] > data["JP"][1] ? "j" : "p"
                        setDisabled(false)
                        navigate("/types/"+primaryType)
                    }
                })
        }
        else if (chosenType === "text"){
            setText(text.replace("\n", ""))
            await fetch(process.env.REACT_APP_BACKEND_LINK + "/text",
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                    method: "POST",
                    body: JSON.stringify({"text": text})
                })
                .then(async (response) => {
                    if (response.ok){
                        let data = await response.json()
                        setMbtiTypes(data)
                        let primaryType = data["IE"][0] > data["IE"][1] ? "i" : "e"
                        primaryType += data["NS"][0] > data["NS"][1] ? "n" : "s"
                        primaryType += data["TF"][0] > data["TF"][1] ? "t" : "f"
                        primaryType += data["JP"][0] > data["JP"][1] ? "j" : "p"
                        setDisabled(false)
                        navigate("/types/"+primaryType)
                    }
                })
        }

    }

    return (
        <main>
            <section className={styles.test}>
                <div className={styles.type_choose}>
                    <p className={chosenType === "user" ? styles.chosen_type : ""}
                        onClick={() => setChosenType("user")}>By username</p>
                    <p>●</p>
                    <p className={chosenType === "text" ? styles.chosen_type : ""}
                       onClick={() => setChosenType("text")}>By text</p>
                </div>
                <form className={styles.test_form}>
                    {chosenType === "user" ?
                    <input type={"text"} className={styles.user_name} value={userName}
                           onChange={e => setUserName(e.target.value)}
                           onFocus={() => setShowNamePlaceholder(false)}
                        onBlur={e => checkUserName(e.target.value)}></input>
                        :
                        <textarea className={styles.textarea} value={text}
                               onChange={e => setText(e.target.value)}
                               onFocus={() => setShowTextPlaceholder(false)}
                               onBlur={e => checkText(e.target.value)}></textarea>
                    }
                        {(chosenType === "user" && showNamePlaceholder ?
                            <p className={styles.placeholder_user}>Enter <span className={"accent"}>Redditor</span> name</p>
                        : null)}
                        {(chosenType === "text" && showTextPlaceholder ?
                            <p className={styles.placeholder_text}>Enter text</p>
                        : null)}
                    <button type={"submit"} className={styles.send} disabled={disabled}
                            onClick={e => send(e)}>{buttonStatus}</button>
                </form>
            </section>
        </main>
    )
}