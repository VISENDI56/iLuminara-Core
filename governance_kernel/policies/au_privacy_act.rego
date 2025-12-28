package iluminara

allow if {
  input.region == "AU"
  input.framework == "AU_PRIVACY_ACT"
  input.data_type != "personal_information"
}
