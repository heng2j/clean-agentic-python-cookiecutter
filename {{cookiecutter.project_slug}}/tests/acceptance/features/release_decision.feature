Feature: Release decisions use explicit evidence

  Scenario: A healthy change is approved
    Given no deterministic gate failed
    And the maximum CRAP score is 11
    And the mutation score is 95
    When the release evidence is evaluated
    Then the release is approved

  Scenario: Weak mutation evidence blocks release
    Given no deterministic gate failed
    And the maximum CRAP score is 12
    And the mutation score is 45
    When the release evidence is evaluated
    Then the release is blocked
    And "mutation score below floor" is a reason
