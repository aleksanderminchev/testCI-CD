// i18n
import './locales/i18n';

// scroll bar
import 'simplebar-react/dist/simplebar.min.css';

// lazy image
import 'react-lazy-load-image-component/src/effects/blur.css';

// slick-carousel
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

// ----------------------------------------------------------------------

import { BrowserRouter } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';

// @mui
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { Button } from '@mui/material';

// redux
import { useState } from 'react';
import { Provider as ReduxProvider } from 'react-redux';
import { store } from './redux/store';

// routes
import Router from './routes';

// theme
import ThemeProvider from './theme';

// locales
import ThemeLocalization from './locales';

// components
import SnackbarProvider from './components/snackbar';
import ScrollToTop from './components/scroll-to-top';
import { MotionLazyContainer } from './components/animate';
import { ThemeSettings, SettingsProvider } from './components/settings';
import { AuthProvider } from './auth/JwtContext';
import LessonPage from './pages/dashboard/lessons/LessonPage';
// ----------------------------------------------------------------------

export default function App() {
  const [urlForLesson, setUrlForLesson] = useState<string>('');
  const [redirectionUrl, setRedirectionUrl] = useState<string>('');
  const [finishLesson, setFinishLesson] = useState(false);
  const [returnForStudent, setReturnForStudent] = useState<boolean>(false);
  const goBackStudent = (isStudent: boolean) => {
    if (isStudent) {
      window.location.replace(redirectionUrl);
    }
  };
  return (
    <AuthProvider>
      <HelmetProvider>
        <ReduxProvider store={store}>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <SettingsProvider>
              <BrowserRouter>
                <ScrollToTop />
                <MotionLazyContainer>
                  <ThemeProvider>
                    <ThemeSettings>
                      <ThemeLocalization>
                        <SnackbarProvider>
                          {urlForLesson ? (
                            <>
                              <Button
                                variant="contained"
                                onClick={() => {
                                  setFinishLesson(true);
                                  // window.location.replace(redirectionUrl)
                                  goBackStudent(returnForStudent);
                                }}
                              >
                                Afslut Lektionen
                              </Button>
                              <LessonPage
                                goBackStudent={setReturnForStudent}
                                urlForLesson={urlForLesson}
                                setRedirectionUrl={setRedirectionUrl}
                                setUrlForLesson={setUrlForLesson}
                                finishLesson={finishLesson}
                                setFinishLesson={setFinishLesson}
                              />
                            </>
                          ) : (
                            <Router
                              setReturnForStudent={setReturnForStudent}
                              urlForLesson={urlForLesson}
                              setUrlForLesson={setUrlForLesson}
                            />
                          )}
                        </SnackbarProvider>
                      </ThemeLocalization>
                    </ThemeSettings>
                  </ThemeProvider>
                </MotionLazyContainer>
              </BrowserRouter>
            </SettingsProvider>
          </LocalizationProvider>
        </ReduxProvider>
      </HelmetProvider>
    </AuthProvider>
  );
}
