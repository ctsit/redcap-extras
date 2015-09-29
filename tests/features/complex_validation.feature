Feature: Allow additional values outside of a specified range
	As a Data Instrument designer,
	I would like to provide additional numerical options outside a range of
		acceptable values
	So that the Abstractor can use the same field in normal and exceptional
		cases.

	Background: Some background
		Given the "Complex Validation" hook has been installed
		And a project exists with a "Demographics" form
		And the "Demographics" form has a "Birth Month" field with a range of 1-12
		And the notes for that field read "Use '<span class=valid>99</span>' for 'Unknown'"

	Scenario: Using an acceptable out-of-range option should not trigger alert
		Given I'm filling out the "Birth Month" field of the "Demographics" form
		 When I enter "99" for "Unknown"
		 Then I should not see the normal "Out of Range" alert.
