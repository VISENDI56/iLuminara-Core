package iluminara

allow if {
  input.region == "NG"
  input.framework == "NG_NDPR"
  input.data_type != "personal_data"
}
