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

function Driver({ info }) {
    return (
        <Grid item>
            <Card>
                <ListItem>
                    <ListItemText
                        primary={`${info.name}`}
                        secondary={
                            info.driving &&
                            `${info.driving.series} - ${info.driving.session_type}`
                        }
                    />
                </ListItem>
            </Card>
        </Grid>
    );
}

function DriverList({ drivers, status }) {
    const elements = drivers.map((d) => (
        <>
            <Driver key={d.name} info={d} />
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
                alignItems="stretch"
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

const WarningTitle = styled(CenteredTitle)`
    color: red;
`;

export default function Drivers() {
    const [status, setStatus] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function get_drivers() {
            let resp = await fetch("/api/drivers");
            let data = await resp.json();
            setStatus(data);
            setError(null);
            setIsLoaded(true);
        }

        function load() {
            get_drivers().catch((error) => {
                setError(error);
                setIsLoaded(true);
            });
        }

        const timer = setInterval(load, 1000);

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
            {error ? (
                <>
                    <br />
                    <WarningTitle variant="h5">API is down</WarningTitle>
                </>
            ) : (
                <>
                    <Driving drivers={online} />
                    <Offline drivers={offline} />
                </>
            )}
        </DriverContainer>
    );
}
