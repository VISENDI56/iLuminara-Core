package iluminara

allow if {
  input.region == "JP"
  input.framework == "JP_APPI"
  input.data_type != "personal_information"
}
