import * as GeoApi from "../api/geo";

class CadastralParcel {
  static fromLatLng({ lat, lng }) {
    return GeoApi.getCadastralParcelFromPos({ lat, lng }).then(
      ({ insee, section, number }) =>
        new CadastralParcel(insee, section, number)
    );
  }

  constructor(insee, section, number) {
    this.insee = parseInt(insee);
    this.section = section;
    this.number = parseInt(number);
  }

  get modelId() {
    return "CADASTRAL_PARCEL";
  }

  json() {
    return {
      insee: this.insee,
      section: this.section,
      number: this.number,
    };
  }

  shape() {
    const myself = this;
    return GeoApi.getCadastralParcelShape(
      this.insee,
      this.section,
      this.number
    ).then(geojson => {
      let feat = geojson["features"][0];
      feat.properties = myself.json();
      feat.properties.type = myself.modelId;
      return feat;
    });
  }
}

export default CadastralParcel;
