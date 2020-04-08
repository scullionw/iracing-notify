import React, { useState, useEffect } from "react";
import partition from "lodash/partition";
import styled from "@emotion/styled";
import {
    Button,
    Paper,
    Typography,
    List,
    ListItem,
    ListItemText,
    Card,
    Grid,
} from "@material-ui/core";

function Driving(props) {
    return <DriverList status="Online" drivers={props.drivers} />;
}

function Offline(props) {
    return <DriverList status="Offline" drivers={props.drivers} />;
}

function Driver(props) {
    return (
        <Grid item>
            <Card>
                <ListItem>
                    <ListItemText
                        primary={props.name}
                        secondary={"Interlagos"}
                    />
                </ListItem>
            </Card>
        </Grid>
    );
}

function DriverList({ drivers, status }) {
    const elements = drivers.map((d) => (
        <>
            <Driver key={d.name} name={d.name} />
        </>
    ));
    return (
        <div>
            <Typography variant="h5">
                <b>{status}</b>
            </Typography>
            <br />
            <Grid
                container
                direction="column"
                justify="center"
                alignItems="left"
                spacing={1}
            >
                {elements}
            </Grid>
            <br />
        </div>
    );
}

const CenteredTitle = styled(Typography)`
    text-align: center;
`;

const DriverContainer = styled.div`
    padding: 10px;
`;

export default function Drivers() {
    const [status, setStatus] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        async function load_drivers() {
            let resp = await fetch("/api/drivers");
            let data = await resp.json();
            setStatus(data);
            setIsLoaded(true);
        }

        load_drivers();

        const timer = setInterval(load_drivers, 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

    if (!isLoaded) {
        return null;
    }

    const [offline, online] = partition(
        status,
        (driver) => driver.driving === null
    );

    return (
        <DriverContainer>
            <CenteredTitle variant="h2">Driver status</CenteredTitle>
            <Driving drivers={online} />
            <Offline drivers={offline} />
        </DriverContainer>
    );
}
