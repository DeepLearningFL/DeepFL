language: PYTHON
name:     "bayesianMain"

variable {
 name: "learning_rate"
 type: FLOAT
 size: 1
 min:  0.0001
 max:  0.2
}

variable {
 name: "L2_value"
 type: FLOAT
 size: 1
 min:  0.0001
 max:  0.05
}

variable {
 name: "dropout_rate"
 type: FLOAT
 size: 1
 min:  0.6
 max:  1
}

variable {
 name: "hiddenNumber"
 type: INT
 size: 1
 min:  10
 max:  37
}

variable {
 name: "batch_size"
 type: INT
 size: 1
 min:  200
 max:  500
}
variable {
 name: "training_epochs"
 type: INT
 size: 1
 min:  1
 max:  200
}
