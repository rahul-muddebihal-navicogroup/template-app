package com.empowermobileappoem4;

// Required by https://reactnavigation.org/docs/getting-started/
import android.os.Bundle;
import com.facebook.react.ReactActivity;

public class MainActivity extends ReactActivity {

  // Required by https://reactnavigation.org/docs/getting-started/
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(null);
  }

  /**
    When Android back button is pressed on Home screen, only minimise the app, not kill it.
    This helps because it keeps the app's current state on next launch.
  */
  @Override
  public void invokeDefaultOnBackPressed() {
    moveTaskToBack(true);
  }

  /**
   * Returns the name of the main component registered from JavaScript. This is used to schedule
   * rendering of the component.
   */
  @Override
  protected String getMainComponentName() {
    return "EmpowerMobileAppOEM4";
  }
}
