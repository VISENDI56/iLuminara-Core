package iluminara

allow if {
  input.region == "ZA"
  input.framework == "POPIA"
  input.data_type != "special_personal_information"
}
