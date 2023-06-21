import React, {useState, useContext} from "react"
import {useNavigate} from "react-router-dom";

import styles from "./Test.module.css"
import {Context} from "../context";
import {Alert, CircularProgress, Snackbar} from "@mui/material";

export function Test(){
    let navigate = useNavigate()
    const {setMbtiTypes} = useContext(Context);
    const [chosenType, setChosenType] = useState("user")
    const [userName, setUserName] = useState("")
    const [text, setText] = useState("")
    const [showNamePlaceholder, setShowNamePlaceholder] = useState(true)
    const [showTextPlaceholder, setShowTextPlaceholder] = useState(true)
    const [textButtonStatus, setTextButtonStatus] = useState("Learn yourself")
    const [userButtonStatus, setUserButtonStatus] = useState("Learn yourself")
    const [textDisabled, setTextDisabled] = useState(false)
    const [userDisabled, setUserDisabled] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")
    const [showError, setShowError] = useState(false)

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

        if (chosenType === "user"){
            setUserName(userName.replace("\n", ""))
            setUserButtonStatus("Loading")
            setUserDisabled(true)
            setTextDisabled(true)
            await fetch(process.env.REACT_APP_BACKEND_LINK + "/user?username="+userName)
                .then(async (response) => {
                    if (response.ok){
                        let data = await response.json()
                        setMbtiTypes(data)
                        let primaryType = data["IE"][0] >= data["IE"][1] ? "i" : "e"
                        primaryType += data["NS"][0] >= data["NS"][1] ? "n" : "s"
                        primaryType += data["TF"][0] >= data["TF"][1] ? "t" : "f"
                        primaryType += data["JP"][0] >= data["JP"][1] ? "j" : "p"
                        setUserDisabled(false)
                        navigate("/types/"+primaryType)
                    }
                    else if(response.status === 400){
                        setErrorMessage(await response.text())
                        setShowError(true)

                        setUserButtonStatus("Learn yourself")
                        setUserDisabled(false)
                        setTextDisabled(false)
                    }
                    else if (response.status === 500){
                        navigate("/error")
                    }
                })
                .catch((error) => {
                    setUserButtonStatus("Learn yourself")
                    setUserDisabled(false)
                    setTextDisabled(false)
                    if (error.message === "Failed to fetch"){
                        navigate("/error")
                    }
                })
        }
        else if (chosenType === "text"){
            setTextButtonStatus("Loading")
            setUserDisabled(true)
            setTextDisabled(true)
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
                        setTextDisabled(false)
                        navigate("/types/"+primaryType)
                    }
                    else if (response.status === 500) {
                        navigate("/error")

                        setTextButtonStatus("Learn yourself")
                        setTextDisabled(false)
                        setUserDisabled(false)
                    }
                })
                .catch((error) => {
                    setTextButtonStatus("Learn yourself")
                    setTextDisabled(false)
                    setUserDisabled(false)
                    if (error.message === "Failed to fetch"){
                        navigate("/error")
                    }
                })
        }

    }

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }

        setShowError(false);
    };

    return (
        <main>
                <Snackbar open={showError} onClose={handleClose} autoHideDuration={4000}
                          anchorOrigin={{vertical: "bottom", horizontal: "center"}}>
                    <Alert onClose={handleClose} severity="error"
                           sx={{ width: '100%', background: "#f44336", borderRadius: "10px"}}>{errorMessage}</Alert>
                </Snackbar>
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
                        {(chosenType === "user" ?
                            <>
                                {showNamePlaceholder ?
                                <p className={styles.placeholder_user}>Enter <span
                                    className={"accent"}>Redditor</span> name</p>
                                : null}
                                <button type={"submit"} className={styles.send} disabled={userName === "" || userDisabled}
                            onClick={e => send(e)}>{userButtonStatus} {userButtonStatus === "Loading" ? <CircularProgress size={12}/> : null}</button>
                            </>
                        : null)}
                        {(chosenType === "text" ?
                            <>
                            { showTextPlaceholder ?
                                <p className={styles.placeholder_text}>Enter text</p>
                                : null}
                                <button type={"submit"} className={styles.send} disabled={text === "" || textDisabled}
                                    onClick={e => send(e)}>{textButtonStatus} {textButtonStatus === "Loading" ? <CircularProgress size={12}/> : null}</button>
                            </>
                        : null)}
                </form>
            </section>
        </main>
    )
}