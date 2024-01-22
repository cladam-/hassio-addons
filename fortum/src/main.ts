require("dotenv").config();

import Hapi from "@hapi/hapi";
import { getConsumption, login } from "./utils";

const init = async () => {
  const server = Hapi.server({
    port: 4321,
    host: "localhost",
  });

  server.route({
    method: "GET",
    path: "/",
    handler: async (request, h) => {
      try {
        const { access_token } = await login();
        const data = await getConsumption(access_token);
        return data;
      } catch (e) {
        console.log(e);
        return e;
      }
    },
  });

  await server.start();
  console.log("Server running on %s", server.info.uri);
};

process.on("unhandledRejection", (err) => {
  console.log(err);
  process.exit(1);
});

init();
