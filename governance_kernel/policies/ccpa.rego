package iluminara

allow if {
  input.region == "US"
  input.framework == "CCPA"
  input.data_type != "personal_information"
}
