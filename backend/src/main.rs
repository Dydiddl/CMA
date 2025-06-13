use actix_web::{web, App, HttpServer, Responder, HttpResponse};
use actix_cors::Cors;
use serde::{Deserialize, Serialize};
use std::sync::Mutex;
use std::collections::HashMap;

#[derive(Debug, Serialize, Deserialize, Clone)]
struct Project {
    id: i32,
    name: String,
    description: String,
    status: String,
    start_date: String,
    end_date: String,
    progress: i32,
}

struct AppState {
    projects: Mutex<HashMap<i32, Project>>,
}

async fn get_projects(data: web::Data<AppState>) -> impl Responder {
    let projects = data.projects.lock().unwrap();
    let projects_vec: Vec<&Project> = projects.values().collect();
    HttpResponse::Ok().json(projects_vec)
}

async fn get_project(
    data: web::Data<AppState>,
    project_id: web::Path<i32>,
) -> impl Responder {
    let projects = data.projects.lock().unwrap();
    match projects.get(&project_id) {
        Some(project) => HttpResponse::Ok().json(project),
        None => HttpResponse::NotFound().finish(),
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let app_state = web::Data::new(AppState {
        projects: Mutex::new(HashMap::new()),
    });

    HttpServer::new(move || {
        let cors = Cors::default()
            .allow_any_origin()
            .allow_any_method()
            .allow_any_header();

        App::new()
            .wrap(cors)
            .app_data(app_state.clone())
            .route("/api/projects", web::get().to(get_projects))
            .route("/api/projects/{id}", web::get().to(get_project))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
} 