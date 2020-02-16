class Project {
  static load(id) {
    return fetch(`/data/${id}/config.json`)
      .then(resp => resp.json())
      .then(cfg => new Project(id, cfg));
  }

  constructor(id, config) {
    this.id = id;
    this.config = config;
  }
}

export default Project;
