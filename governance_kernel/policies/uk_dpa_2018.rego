package iluminara

allow if {
  input.region == "UK"
  input.framework == "UK_DPA_2018"
  input.data_type != "special_category_data"
}
