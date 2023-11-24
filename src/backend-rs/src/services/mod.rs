extern crate diesel;
extern crate rocket;
// use crate::models::{Account, NewAccount};
// use crate::schema;
use diesel::pg::PgConnection;
use diesel::prelude::*;
use dotenvy::dotenv;
// use rocket::response::{status::Created, Debug};
// use rocket::serde::{json::Json, Deserialize, Serialize};
// use rocket::{get, post};
// use rocket_dyn_templates::{context, Template};
use std::env;

pub fn establish_connection_pg() -> PgConnection {
    dotenv().ok();
    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    PgConnection::establish(&database_url)
        .unwrap_or_else(|_| panic!("Error connecting to {}", database_url))
}

pub mod accounts;