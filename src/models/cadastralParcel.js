import * as GeoApi from '../api/geo';

class CadastralParcel {
  static fromLatLng({ lat, lng }) {
    return GeoApi.getCadastralParcelFromPos({ lat, lng })
      .then(({ insee, section, number }) => new CadastralParcel(insee, section, number));
  }

  constructor(insee, section, number) {
    this.insee = parseInt(insee);
    this.section = section;
    this.number = parseInt(number);
  }

  json() {
    return {
      insee: this.insee,
      section: this.section,
      number: this.number,
    };
  }

  shape() {
    return GeoApi.getCadastralParcelShape(this.insee, this.section, this.number);
  }
}

export default CadastralParcel;
