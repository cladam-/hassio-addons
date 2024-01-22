import { AuthResponse } from "./types";
import fs from "fs";

export const safeParseInt = (str: string | undefined) =>
  str === undefined ? undefined : Number.parseInt(str, 10);

const AUTH_URL = "https://retail-lisa-eu-auth.herokuapp.com/api/login";
const CONSUMPTION_URL = (customer: number, point: number) =>
  `https://retail-lisa-eu-prd-energyflux.herokuapp.com/api/consumption/customer/${customer}/meteringPoint/${point}`;

const username = process.env.FORTUM_EMAIL;
const password = process.env.PASSWORD;
const headers = {
  "User-Agent":
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
  Accept: "application/json",
  "Accept-Language": "en-US,sv-SE;q=0.7,en;q=0.3",
  "Content-Type": "application/x-www-form-urlencoded",
  "Sec-Fetch-Dest": "empty",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Site": "cross-site",
};

export async function login() {
  try {
    const file = fs.readFileSync("./.cache");
    console.log("Using cached credentials");
    return JSON.parse(file.toString());
  } catch {
    const response = await fetch(AUTH_URL, {
      credentials: "omit",
      headers,
      referrer: "https://www.mittfortum.se/",
      body: `username=${username}&password=${password}`,
      method: "POST",
      mode: "cors",
    });
    if (response.status >= 200 && response.status < 400) {
      const json: AuthResponse = await response.json();
      fs.writeFileSync("./.cache", JSON.stringify(json));
      return json;
    } else {
      throw new Error(await response.text());
    }
  }
}

export async function getConsumption(token: string) {
  const customer = safeParseInt(process.env.CUSTOMER);
  const point = safeParseInt(process.env.POINT);
  const now = Date.now();
  const week = 1000 * 60 * 60 * 24 * 7;
  const to = new Date(now).toISOString().slice(0, 10);
  const from = new Date(now - week).toISOString().slice(0, 10);
  const body = {
    from,
    to,
    resolution: "hourly",
    postalAddress: process.env.POSTAL_ADDRESS,
    postOffice: process.env.POST_OFFICE,
  };

  try {
    const response = await fetch(CONSUMPTION_URL(customer!, point!), {
      credentials: "include",
      headers: {
        "User-Agent":
          "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        Accept: "application/json",
        "Accept-Language": "en-US,sv-SE;q=0.7,en;q=0.3",
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
      },
      referrer: "https://www.mittfortum.se/",
      body: JSON.stringify(body),
      method: "POST",
      mode: "cors",
    });
    if (response.status > 399) {
      throw new Error("Bad Auth");
    }
    return response.json();
  } catch (e) {
    if (e instanceof Error && e.message === "Bad Auth") {
      fs.unlinkSync("./.cache");
      console.log("Refetching creds");
      const { access_token } = await login();
      return getConsumption(access_token);
    }
    console.log(e);
  }
}
