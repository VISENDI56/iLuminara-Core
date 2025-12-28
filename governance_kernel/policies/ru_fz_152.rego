package iluminara

allow if {
  input.region == "RU"
  input.framework == "RU_FZ_152"
  input.data_type != "personal_data"
}
