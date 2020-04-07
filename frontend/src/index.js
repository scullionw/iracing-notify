import React from "react";
import ReactDOM from "react-dom";
import * as serviceWorker from "./serviceWorker";
import "bootstrap/dist/css/bootstrap.min.css";
import { Global, css } from "@emotion/core";
import CssBaseline from "@material-ui/core/CssBaseline";
import Drivers from "./Drivers";

ReactDOM.render(
    <React.StrictMode>
        <CssBaseline />
        <Global
            styles={css`
                body {
                    margin: 0;
                    /* margin: 0 auto; */
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                        "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans",
                        "Droid Sans", "Helvetica Neue", sans-serif;
                    -webkit-font-smoothing: antialiased;
                    -moz-osx-font-smoothing: grayscale;
                    width: auto;

                    padding: 0 20px 20px 20px;
                    /* border: 5px solid black; */
                }
            `}
        />
        <Drivers />
    </React.StrictMode>,
    document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
