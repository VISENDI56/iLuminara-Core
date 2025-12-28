package iluminara

allow if {
  input.region == "BR"
  input.framework == "BR_LAW"
  input.data_type != "restricted_data"
}
